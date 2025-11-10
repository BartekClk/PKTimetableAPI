from sqlalchemy import Column, Date, Integer, String, ForeignKey, Time
from sqlalchemy.orm import relationship, declarative_base
from database import Base

class Syllabus(Base):
    __tablename__ = "syllabus"
    id = Column(Integer, primary_key=True, index=True)
    shortName = Column(String(100))
    hashTag = Column(String(100))
    name = Column(String(100))

class Hours(Base):
    __tablename__ = "hours"
    id = Column(Integer, primary_key=True, index=True)
    start = Column(Time)
    end = Column(Time)

class Timetable11k1(Base):
    __tablename__ = "timetable_11k1"
    id = Column(Integer, primary_key=True, index=True)
    day = Column(Integer)
    hour = Column(Integer, ForeignKey("hours.id"))
    syllabusID = Column(Integer, ForeignKey("syllabus.id"))
    lessonType = Column(String(50))
    week = Column(String(50))
    lecturer = Column(String(100))
    lecturerLink = Column(String(200))
    hall = Column(String(100))
    hallLink = Column(String(200))
    altName = Column(String(100))

    syllabus = relationship("Syllabus", backref="timetable_11k1")
    hours = relationship("Hours", backref="timetable_11k1")

class Timetable11k2(Base):
    __tablename__ = "timetable_11k2"
    id = Column(Integer, primary_key=True, index=True)
    day = Column(Integer)
    hour = Column(Integer, ForeignKey("hours.id"))
    syllabusID = Column(Integer, ForeignKey("syllabus.id"))
    lessonType = Column(String(50))
    week = Column(String(50))
    lecturer = Column(String(100))
    lecturerLink = Column(String(200))
    hall = Column(String(100))
    hallLink = Column(String(200))
    altName = Column(String(100))

    syllabus = relationship("Syllabus", backref="timetable_11k2")
    hours = relationship("Hours", backref="timetable_11k2")

class Changes(Base):
    __tablename__ = "changes_11k1"
    id = Column(Integer, primary_key=True, index=True)
    action = Column(Integer)
    syllabusID = Column(Integer)
    start = Column(Date)
    end = Column(Date)
    operation = Column(String)