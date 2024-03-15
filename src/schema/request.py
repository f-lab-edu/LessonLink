from pydantic import BaseModel
from datetime import date

class CreateStudentRequest(BaseModel):
    id: str
    pw: str = None
    name: str = None
    contact: str = None
    email: str = None
    birth_date: date = None
    gender: str = None
    join_date: date = date.today()


class CreateInstructorRequest(BaseModel):
    id: str
    pw: str = None
    name: str = None
    contact: str = None
    email: str = None

class UpdatePasswordRequest(BaseModel):
    pw: str

class CreateCourseRequest(BaseModel):
    id: int
    name: str = None
    description: str = None
    start_date: date = None
    end_date: date = None
    instructor_id: str = None

class UpdateCourseRequest(BaseModel):
    id: int
    name: str = None
    description: str = None
    start_date: date = None
    end_date: date = None
    instructor_id: str = None