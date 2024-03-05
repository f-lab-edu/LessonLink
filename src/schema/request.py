from pydantic import BaseModel
from datetime import date

class StudentRequest(BaseModel):
    student_id: str
    student_pw: str = None
    student_name: str = None
    student_contact: str = None
    student_email: str = None
    student_birth_date: date = None
    student_gender: str = None
    join_date: date = date.today()