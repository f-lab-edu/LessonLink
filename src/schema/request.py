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
    instructor_id: str
    instructor_pw: str = None
    instructor_name: str = None
    instructor_contact: str = None
    instructor_email: str = None

