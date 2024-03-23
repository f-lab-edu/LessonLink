from pydantic import BaseModel
from datetime import date, datetime, time
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
    instructors: List[InstructorSchema]


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
    courses: List[CourseSchema]


class ClassroomSchema(BaseModel):
    name: str
    capacity: int = None
    location: str = None
    building_name: str = None

    class Config:
        orm_mode = True
        from_attributes = True


class ClassroomListSchema(BaseModel):
    courses: List[ClassroomSchema]


class ScheduleSchema(BaseModel):
    course_id: int = None
    classroom_id: int = None
    start_time: time = None
    end_time: time = None
    course_date: date = None

    class Config:
        orm_mode = True
        from_attributes = True

class ScheduleListSchema(BaseModel):
    courses: List[ScheduleSchema]


class ReservationSchema(BaseModel):
    student_id: str
    course_id: int
    schedule_id: int
    reservated_date: date
    reservated_time: datetime
    status: str
    notes: str = None

    class Config:
        orm_mode = True
        from_attributes = True


class ReservationSchema(BaseModel):
    courses: List[ReservationSchema]
