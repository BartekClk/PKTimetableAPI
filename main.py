from datetime import date, datetime
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
import models
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

from weekType import Week

from components.timetableRowGen import timetableRow
from components.mergeLessons import mergeLessons
from components.fillBreaks import fillBreaks
from components.sortTimetable import sortTimetable

app = FastAPI()
# --- CORS ---
# origins = [
#     "http://localhost:5173",
#     "*"
#     # lub "*" żeby pozwolić wszystkim
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
                  jang: int = None,
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

    if group == "1" or group == "11k1":
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

        changesData = []
        if changes == True:
            changesData = db.query(models.Changes_11k1).all()

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
    elif group == "2" or group == "11k2":
        data = db.query(models.Timetable11k2).options(
            joinedload(models.Timetable11k2.syllabus),
            joinedload(models.Timetable11k2.hours)
            ).all()
        hours_ = db.query(models.Hours).all()
        hours = {}
        for row in hours_:
            hours[row.id] = {
                "start":row.start,
                "end":row.end
            }

        changesData = []
        if changes == True:
            changesData = db.query(models.Changes_11k2).all()

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
        raise HTTPException(status_code=400, detail="Invalid group parameter: 1/11k1, 2/11k2,  are allowed")
    
@app.get("/weektype")
def getWeektype(type:str = None):
    week = Week()
    if type is not None and type == "exact":
        return [{"weekType":week.get()}]
    else:
        return [{"weekType":week.get(earlyChange=True)}]
    
@app.get("/hours")
def getHours():
    return [{"id":1,"start":"07:30","end":"08:15"},{"id":2,"start":"08:15","end":"09:00"},{"id":3,"start":"09:15","end":"10:00"},{"id":4,"start":"10:00","end":"10:45"},{"id":5,"start":"11:00","end":"11:45"},{"id":6,"start":"11:45","end":"12:30"},{"id":7,"start":"12:45","end":"13:30"},{"id":8,"start":"13:30","end":"14:15"},{"id":9,"start":"14:30","end":"15:15"},{"id":10,"start":"15:15","end":"16:00"},{"id":11,"start":"16:15","end":"17:00"},{"id":12,"start":"17:00","end":"17:45"},{"id":13,"start":"18:00","end":"18:45"},{"id":14,"start":"18:45","end":"19:30"},{"id":15,"start":"19:45","end":"20:30"},{"id":16,"start":"20:30","end":"21:15"}]

@app.get("/colors")
def getColors(db: Session = Depends(get_db)):
    colors = db.query(models.Colors).all()

    result = {}
    for row in colors:
        result[row.id] = {
            "name":row.name,
            "color":row.color,
            "gradient":row.gradient,
        }

    return [result]

@app.get("/available_fields")
def getFields(db: Session = Depends(get_db)):
    fields = db.query(models.AvailableFields).all()

    result = []
    for row in fields:
        result.append({
            "name":row.name,
            "value":row.value,
        })

    return result