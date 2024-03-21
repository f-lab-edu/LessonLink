from pydantic import BaseModel
from datetime import date, datetime

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
    name: str = None
    description: str = None
    start_date: date = None
    end_date: date = None
    instructor_id: str = None
    

class CreateClassroomRequest(BaseModel):
    name: str
    capacity: int = None
    location: str = None
    building_name: str = None


class CreateScheduleRequest(BaseModel):
    course_id: int = None
    classroom_id: int = None
    start_time: datetime = None
    end_time: datetime = None
    course_date: date = None


class CreateReservationRequest(BaseModel):
    student_id: str
    course_id: int
    schedule_id: int
    reservated_date: date
    reservated_time: datetime
    status: str
    notes: str = None