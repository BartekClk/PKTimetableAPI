from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
import models
from database import SessionLocal, engine

from weekType import Week

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/timetable/{group}")
def get_timetable(group: str, 
                  day: int = None,
                  lab: int = None,
                  klab: int = None,
                  week: str = None,
                  merge: bool = False,
                  fill: bool = False,
                  db: Session = Depends(get_db)):
    
    week_ = Week()
    if week is not None:
        if week.lower() == "auto":
            week = week_.get(earlyChange=True)
        elif week.lower() == "autoexact":
            week = week_.get() 
            print(week)

    if group == "all":
        data1 = db.query(models.Timetable11k1).options(joinedload(models.Timetable11k1.syllabus)).all()
        data2 = db.query(models.Timetable11k2).options(joinedload(models.Timetable11k2.syllabus)).all()

        result = [] 
        result1 = []
        result2 = []

        for row in data1:
            el = timetableRow(row, day, lab, klab, week)
            if el is not None: result1.append(el)

        for row in data2:
            el = timetableRow(row, day, lab, klab, week)
            if el is not None: result2.append(el)

        result1 = sorted(result1, key=lambda x:x['day'])
        result2 = sorted(result2, key=lambda x:x['day'])

        result.append({"11k1": result1})
        result.append({"11k2": result2})

        return result
    elif group == "1":
        data = db.query(models.Timetable11k1).options(
            joinedload(models.Timetable11k1.syllabus),
            joinedload(models.Timetable11k1.hours)
            ).all()
        hours_ = db.query(models.Hours).all()
        hours = {}
        for row in hours_:
            hours[row.id] = {
                "start":row.start,
                "end":row.end
            }

        result = []
        for row in data:
            el = timetableRow(row, day, lab, klab, week)
            if el is not None: result.append(el)

        if fill and lab is not None and klab is not None and week is not None:
            result = fillBreaks(result, hours)

        result = sortTimetable(result)

        if merge and lab is not None and klab is not None and week is not None:
            result = mergeLessons(result, hours)

        return result
    elif group == "2":
        data = db.query(models.Timetable11k1).options(
            joinedload(models.Timetable11k1.syllabus),
            joinedload(models.Timetable11k1.hours)
            ).all()
        hours_ = db.query(models.Hours).all()
        hours = {}
        for row in hours_:
            hours[row.id] = {
                "start":row.start,
                "end":row.end
            }

        result = []
        for row in data:
            el = timetableRow(row, day, lab, klab, week)
            if el is not None: result.append(el)

        if fill and lab is not None and klab is not None and week is not None:
            result = fillBreaks(result, hours)

        result = sortTimetable(result)

        if merge and lab is not None and klab is not None and week is not None:
            result = mergeLessons(result, hours)

        return result
    else:
        raise HTTPException(status_code=400, detail="Invalid group parameter: all, 1, 2 are allowed")
    
def timetableRow(row, day = None, lab = None, klab = None, week=None):
    data = {
        "id": row.id,
        "day": row.day,
        "hour": row.hour,
        "length": 1,
        "start": str(row.hours.start)[:-3],
        "end": str(row.hours.end)[:-3],
        "syllabusID": row.syllabusID,
        "syllabus": row.syllabus.name if row.syllabus else None,
        "lessonGroup": row.lessonType[-1:] if (len(row.lessonType) > 1 and len(row.lessonType)<4) else (row.lessonType[-2:] if (len(row.lessonType) > 3 and len(row.lessonType)<5) else ""),
        "lessonType": row.lessonType[:1] if len(row.lessonType) > 1 else "",
        "lessonTypeFull": row.lessonType,
        "week": row.week,
        "lecturer": row.lecturer,
        "lecturerLink": row.lecturerLink,
        "hall": row.hall,
        "hallLink": row.hallLink,
        "altName": row.altName,
    }
    if data is not None and day is not None and data["day"] != day: data = None
    if data is not None and week is not None and week is not None and data["week"].lower() != week.lower(): data = None
    if data is not None and lab is not None and data["lessonType"] == "L" and data["lessonGroup"] != str(lab): data = None
    if data is not None and klab is not None and data["lessonType"] == "K" and data["lessonGroup"] != str(klab): data = None
    return data

def mergeLessons(table, hours):
    if not table:
        return []
    
    merged = []
    i = 0
    
    while i < len(table):
        current = table[i]
        lesson_length = 1
        
        if (i + 1 < len(table) and 
            current["syllabusID"] == table[i + 1]["syllabusID"] and
            current["week"] == table[i + 1]["week"] and
            current["lessonTypeFull"] == table[i + 1]["lessonTypeFull"] and
            current["lecturer"] == table[i + 1]["lecturer"] and
            current["hall"] == table[i + 1]["hall"] and
            current["hour"] + 1 == table[i + 1]["hour"]):
            
            lesson_length = 2
            i += 1
        else:
            pass
        
        merged_lesson = current.copy()
        merged_lesson["length"] = lesson_length
        if merged_lesson["id"]!=-1:
            merged_lesson["end"] = str(hours[int(merged_lesson["hour"]+(lesson_length-1))]["end"])[:-3]
        else:
            merged_lesson["end"] = str(table[i]["end"])
            merged_lesson["exactEnd"] = str(table[i]["exactEnd"])
        merged.append(merged_lesson)
        
        i += 1
    
    return merged

def fillBreaks(table, hours):
    def findLesson(timetable, day, hour):
        return next(
            (lesson for lesson in timetable if lesson['day'] == day and lesson['hour'] == hour), 
            None
        )
    
    filled = table.copy()

    week = []
    nhours = 16
    for d in range(1,6):
        day = []
        for h in range(1,nhours):
            lesson = findLesson(table, d, h)
            day.append(lesson if lesson == None else lesson["syllabusID"])
            if h == nhours-1:
                for i in range(1,nhours):
                    if day[-1] == None: day.pop()
                    else: break
        
        i = 0
        for el in day:
            if el == None:
                start = None
                end = None
                
                if i>0:
                    if str(hours[i+1]["start"]) != str(hours[i]["end"]):
                        start = str(hours[i]["end"])        

                if i+2<=nhours:
                    if str(hours[i+1]["end"]) != str(hours[i+2]["start"]):
                        end = str(hours[i+2]["start"])

                filled.append({
                    "id": -1,
                    "day": d,
                    "hour": i+1,
                    "length": 1,
                    "start": str(hours[i+1]["start"])[:-3],
                    "exactStart": start[:-3] if start != None else str(hours[i+1]["start"])[:-3],
                    "end": str(hours[i+1]["end"])[:-3],
                    "exactEnd": end[:-3] if end != None else str(hours[i+1]["start"])[:-3],
                    "syllabusID": 2,
                    "syllabus": "Przerwa",
                    "lessonGroup": "",
                    "lessonType": "",
                    "lessonTypeFull": "",
                    "week": "",
                    "lecturer": "",
                    "lecturerLink": "",
                    "hall": "",
                    "hallLink": "",
                    "altName": "",
                })

            i+=1
        
        week.append(day)

    return filled

def sortTimetable (timetable):
    return sorted(timetable, key=lambda x: (x.get('day', 0), x.get('hour', 0)))

@app.get("/weektype")
def get_timetable(type:str = None):
    week = Week()
    if type is not None and type == "exact":
        return [{"weekType":week.get()}]
    else:
        return [{"weekType":week.get(earlyChange=True)}]