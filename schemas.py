# schemas.py
from typing import Optional
from pydantic import BaseModel

class SyllabusBase(BaseModel):
    id: int
    shortName: str
    hashTag: Optional[str] = ""
    Name: Optional[str] = ""
    
    class Config:
        from_attributes = True  # Zamiast orm_mode dla nowszych wersji Pydantic

class TimetableBase(BaseModel):
    id: int
    day: int
    hour: int
    length: int
    syllabusID: int
    syllabus: Optional[SyllabusBase] = None
    lessonGroup: Optional[str] = None
    lessonType: Optional[str] = None
    lessonTypeFull: Optional[str] = None
    week: Optional[str] = None
    lecturerShort: Optional[str] = None
    lecturerLink: Optional[str] = None
    hall: Optional[str] = None
    hallLink: Optional[str] = None
    altName: Optional[str] = None

    class Config:
        from_attributes = True  # Zamiast orm_mode dla nowszych wersji Pydantic