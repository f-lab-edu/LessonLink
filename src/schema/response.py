from pydantic import BaseModel
from datetime import date
from typing import List

class StudentSchema(BaseModel):
    id: str
    pw: str = None
    name: str = None
    contact: str = None
    email: str = None
    birth_date: date = None
    gender: str = None
    join_date: date = date.today()

    class Config:
        orm_mode = True
        from_attributes = True

class StudentListSchema(BaseModel):
    students: List[StudentSchema]

class InstructorSchema(BaseModel):
    id: str
    pw: str = None
    name: str = None
    contact: str = None
    email: str = None

    class Config:
        orm_mode = True
        from_attributes = True

class InstructorListSchema(BaseModel):
    students: List[InstructorSchema]

class CourseSchema(BaseModel):
    id: int
    name: str = None
    description: str = None
    start_date: date = None
    end_date: date = None
    instructor_id: str = None

    class Config:
        orm_mode = True
        from_attributes = True

class CourseListSchema(BaseModel):
    students: List[CourseSchema]