from pydantic import BaseModel
from datetime import date
from typing import List

class StudentSchema(BaseModel):
    student_id: str
    student_pw: str = None
    student_name: str = None
    student_contact: str = None
    student_email: str = None
    student_birth_date: date = None
    student_gender: str = None
    join_date: date = date.today()

    class Config:
        orm_mode = True
        from_attributes = True

class StudentListSchema(BaseModel):
    students: List[StudentSchema]

class InstructorSchema(BaseModel):
    instructor_id: str
    instructor_pw: str = None
    instructor_name: str = None
    instructor_contact: str = None
    instructor_email: str = None
    subject: str = None

    class Config:
        orm_mode = True
        from_attributes = True

class InstructorListSchema(BaseModel):
    students: List[InstructorSchema]