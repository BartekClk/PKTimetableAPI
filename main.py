from datetime import date, datetime
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
import models
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

from weekType import Week

app = FastAPI()
# --- CORS ---
origins = [
    "http://localhost:5173",  # adres Twojego Reacta
    # lub "*" żeby pozwolić wszystkim
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- koniec CORS ---

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/timetable/{group}")
def get_timetable(group: str, 
                  day: str = None,
                  lab: int = None,
                  klab: int = None,
                  week: str = None,
                  merge: bool = False,
                  fill: bool = False,
                  changes: bool = False,
                  db: Session = Depends(get_db)):
    
    week_ = Week()
    if week is not None:
        if week.lower() == "auto":
            week = week_.get(earlyChange=True)
        elif week.lower() == "autoexact":
            week = week_.get() 

    if day is not None:
        if day.lower() == "auto":
            day = date.today().isoweekday()
        else:
            try:
                int(day)
                day = int(day)
            except:
                day = None

    changesData = []
    if changes == True:
        changesData = db.query(models.Changes).all()

    if group == "all":
        data1 = db.query(models.Timetable11k1).options(joinedload(models.Timetable11k1.syllabus)).all()
        data2 = db.query(models.Timetable11k2).options(joinedload(models.Timetable11k2.syllabus)).all()

        result = [] 
        result1 = []
        result2 = []

        for row in data1:
            el = timetableRow(row, day, lab, klab, week, changes, [])
            if el is not None: result1.append(el)

        for row in data2:
            el = timetableRow(row, day, lab, klab, week, changes, [])
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
            el = timetableRow(row, day, lab, klab, week, changes, changesData)
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
            el = timetableRow(row, day, lab, klab, week, changes, [])
            if el is not None: result.append(el)

        if fill and lab is not None and klab is not None and week is not None:
            result = fillBreaks(result, hours)

        result = sortTimetable(result)

        if merge and lab is not None and klab is not None and week is not None:
            result = mergeLessons(result, hours)

        return result
    else:
        raise HTTPException(status_code=400, detail="Invalid group parameter: all, 1, 2 are allowed")
    
def timetableRow(row, day, lab, klab, week, changes, changesData):
    data = {
        "id": row.id,
        "day": row.day,
        "hour": row.hour,
        "length": 1,
        "start": str(row.hours.start)[:-3],
        "end": str(row.hours.end)[:-3],
        "syllabusID": row.syllabusID,
        "syllabus": row.syllabus.name if row.syllabus else None,
        "lessonGroup": "",
        "lessonType": "",
        "lessonTypeFull": row.lessonType,
        "week": row.week,
        "lecturer": row.lecturer,
        "lecturerLink": row.lecturerLink,
        "hall": row.hall,
        "hallLink": row.hallLink,
        "altName": row.altName,
    }

    if changes is not None:
        for row in changesData:
            today = date.today()
            start = row.start
            end = row.end
            if (start - today).days <= 0 and (end - today).days >= 0:
                if data is not None and row.action == 1 and data["syllabusID"] == row.syllabusID: data = None
                if data is not None and row.action == 2 and data["syllabusID"]==row.syllabusID:
                    op = row.operation
                    if op.find("^") != -1:
                        day_ = int(op[op.find("^")+1])
                        hours = op[op.find("@")+1:]
                        hours = hours[0:hours.find("@")].split(",")
                        i=0
                        for el in hours:
                            hours[i]=int(hours[i])
                            i+=1

                        content = op[op.find("|")+1:]
                        content = content[0:content.find("|")]
                        param = content.split(">")[0]
                        content = content.split(">")[1]

                        if day_ == data["day"]:
                            try:
                                hours.index(data["hour"])
                                data[param] = content
                            except:
                                continue
    
    if data is not None and day is not None and data["day"] != day: data = None

    if data is not None: 
        data["lessonGroup"] = data["lessonTypeFull"][-1:] if (len(data["lessonTypeFull"]) > 1 and len(data["lessonTypeFull"])<4) else (data["lessonTypeFull"][-2:] if (len(data["lessonTypeFull"]) > 3 and len(data["lessonTypeFull"])<5) else "")
        data["lessonType"] = data["lessonTypeFull"][:1] if len(data["lessonTypeFull"]) > 1 else ""
        
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

        while (
            i + lesson_length < len(table)
            and current["syllabusID"] == table[i + lesson_length]["syllabusID"]
            and current["week"] == table[i + lesson_length]["week"]
            and current["lessonTypeFull"] == table[i + lesson_length]["lessonTypeFull"]
            and current["lecturer"] == table[i + lesson_length]["lecturer"]
            and current["hall"] == table[i + lesson_length]["hall"]
            and current["hour"] + lesson_length == table[i + lesson_length]["hour"]
            and current["lessonTypeFull"] == table[i + lesson_length]["lessonTypeFull"]
        ):
            lesson_length += 1

        merged_lesson = current.copy()
        merged_lesson["length"] = lesson_length

        if merged_lesson["id"] != -1:
            merged_lesson["end"] = str(hours[int(merged_lesson["hour"] + (lesson_length - 1))]["end"])[:-3]
        else:
            merged_lesson["end"] = str(table[i + lesson_length - 1]["end"])
            merged_lesson["exactEnd"] = str(table[i + lesson_length - 1]["exactEnd"])

        merged.append(merged_lesson)
        i += lesson_length 

    return merged

def fillBreaks(table, hours):
    def findLesson(timetable, day, hour):
        return next(
            (lesson for lesson in timetable if lesson['day'] == day and lesson['hour'] == hour), 
            None
        )
    
    filled = table.copy()
    nhours = 16 

    for d in range(1, 6): 
        day_schedule = []
        for h in range(1, nhours):
            lesson = findLesson(table, d, h)
            day_schedule.append(lesson if lesson is None else lesson["syllabusID"])

        while day_schedule and day_schedule[-1] is None:
            day_schedule.pop()

        has_lesson_before = False
        for i, el in enumerate(day_schedule):
            if el is None:
                if not has_lesson_before:
                    continue

                start = None
                end = None
                if i > 0 and str(hours[i+1]["start"]) != str(hours[i]["end"]):
                    start = str(hours[i]["end"])
                if i + 2 <= nhours and str(hours[i+1]["end"]) != str(hours[i+2]["start"]):
                    end = str(hours[i+2]["start"])

                filled.append({
                    "id": -1,
                    "day": d,
                    "hour": i+1,
                    "length": 1,
                    "start": str(hours[i+1]["start"])[:-3],
                    "exactStart": start[:-3] if start is not None else str(hours[i+1]["start"])[:-3],
                    "end": str(hours[i+1]["end"])[:-3],
                    "exactEnd": end[:-3] if end is not None else str(hours[i+1]["start"])[:-3],
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
            else:
                has_lesson_before = True

    return filled

def sortTimetable (timetable):
    return sorted(timetable, key=lambda x: (x.get('day', 0), x.get('hour', 0)))

@app.get("/weektype")
def getWeektype(type:str = None):
    week = Week()
    if type is not None and type == "exact":
        return [{"weekType":week.get()}]
    else:
        return [{"weekType":week.get(earlyChange=True)}]