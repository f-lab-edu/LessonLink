from pydantic import BaseModel
from datetime import date, time


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
    cost: int


class UpdateCourseRequest(BaseModel):
    name: str = None
    description: str = None
    start_date: date = None
    end_date: date = None
    instructor_id: str = None
    cost: int


class CreateClassroomRequest(BaseModel):
    name: str
    capacity: int = None
    location: str = None
    building_name: str = None


class UpdateClassroomRequest(BaseModel):
    name: str
    capacity: int = None
    location: str = None
    building_name: str = None


class CreateScheduleRequest(BaseModel):
    course_id: int = None
    classroom_id: int = None
    start_time: time = None
    end_time: time = None
    course_date: date = None


class UpdateScheduleRequest(BaseModel):
    course_id: int = None
    classroom_id: int = None
    start_time: time = None
    end_time: time = None
    course_date: date = None


class CreateReservationRequest(BaseModel):
    student_id: str
    schedule_id: int
    reservated_date: date
    reservated_time: time
    status: str
    notes: str = None


class UpdateReservationRequest(BaseModel):
    student_id: str
    schedule_id: int
    reservated_date: date
    reservated_time: time
    status: str
    notes: str = None


class LogInRequest(BaseModel):
    id: str
    pw: str = None


class PaymentsRequest(BaseModel):
    uid: str
    name: str
    amount: int
    status: str
    is_paid_ok: bool
    student_id: str


class PutInBucketRequest(BaseModel):
    id: str
    course_id: int = None


class PutOutBucketRequest(BaseModel):
    course_id: int = None