from decimal import Decimal
from sqlalchemy import Boolean, Column, String, Date, Integer, ForeignKey, Time, Numeric
from sqlalchemy.orm import declarative_base, relationship

from schema.request import (
    CreateCourseRequest, CreateInstructorRequest,
    CreateStudentRequest, CreateClassroomRequest,
    CreateReservationRequest, CreateScheduleRequest
)
import bcrypt

Base = declarative_base()


class Students(Base):
    __tablename__ = "students"

    id: Column = Column(String(50), primary_key=True)
    pw: Column = Column(String(255))
    name: Column = Column(String(20))
    contact: Column = Column(String(20))
    email: Column = Column(String(50))
    birth_date: Column = Column(Date)
    gender: Column = Column(String(10))
    join_date: Column = Column(Date)

    reservations = relationship("Reservations", back_populates="students")
    payments = relationship("Payments", back_populates="students")

    def __repr__(self):
        return "".join((
            f"Students(",
            f"id={self.id!r}, ",
            f"pw={self.pw!r}, ",
            f"name={self.name!r}, ",
            f"contact={self.contact!r}, ",
            f"email={self.email}, ",
            f"birth_date={self.birth_date!r}, ",
            f"gender={self.gender!r}, ",
            f"join_date={self.join_date!r}",
            f")"
        ))

    @classmethod
    def create(cls, request: CreateStudentRequest) -> "Students":

        encrypted_pw = bcrypt.hashpw(request.pw.encode(), bcrypt.gensalt())

        return cls(
            id=request.id,
            pw=encrypted_pw.decode(),
            name=request.name,
            contact=request.contact,
            email=request.email,
            birth_date=request.birth_date,
            gender=request.gender,
            join_date=request.join_date
        )


class Instructors(Base):
    __tablename__ = "instructors"

    id: Column = Column(String(50), primary_key=True)
    pw: Column = Column(String(255))
    name: Column = Column(String(20))
    contact: Column = Column(String(20))
    email: Column = Column(String(50))

    courses = relationship("Courses", back_populates="instructors")

    def __repr__(self):
        return "".join((
            f"Instructors(",
            f"id={self.id!r}, ",
            f"pw={self.pw!r}, ",
            f"name={self.name!r}, ",
            f"contact={self.contact}, ",
            f"email={self.email!r}, ",
            f")"
        ))

    @classmethod
    def create(cls, request: CreateInstructorRequest) -> "Instructors":

        encrypted_pw = bcrypt.hashpw(request.pw.encode(), bcrypt.gensalt())

        return cls(
            id=request.id,
            pw=encrypted_pw,
            name=request.name,
            contact=request.contact,
            email=request.email,
        )


class Courses(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    description = Column(String(256))
    start_date = Column(Date)
    end_date = Column(Date)
    instructor_id = Column(String(50), ForeignKey('instructors.id'))
    cost = Column(Integer)

    instructors = relationship("Instructors", back_populates="courses")
    schedules = relationship("Schedules", back_populates="courses")

    @classmethod
    def create(cls, request: CreateCourseRequest) -> "Courses":

        return cls(
            id=request.id,
            name=request.name,
            description=request.description,
            start_date=request.start_date,
            end_date=request.end_date,
            instructor_id=request.instructor_id,
            cost=request.cost
        )


class Classrooms(Base):
    __tablename__ = "classrooms"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    capacity = Column(Integer, nullable=True)
    location = Column(String(100), nullable=True)
    building_name = Column(String(100), nullable=True)

    schedules = relationship("Schedules", back_populates="classrooms")

    @classmethod
    def create(cls, request: CreateClassroomRequest) -> "Classrooms":

        return cls(
            name=request.name,
            capacity=request.capacity,
            location=request.location,
            building_name=request.building_name
        )


class Schedules(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=True)
    classroom_id = Column(Integer, ForeignKey('classrooms.id'), nullable=True)
    start_time = Column(Time, nullable=True)
    end_time = Column(Time, nullable=True)
    course_date = Column(Date, nullable=True)

    courses = relationship("Courses", back_populates="schedules")
    classrooms = relationship("Classrooms", back_populates="schedules")
    reservations = relationship("Reservations", back_populates="schedules")

    @classmethod
    def create(cls, request: CreateScheduleRequest) -> "Schedules":

        return cls(
            course_id=request.course_id,
            classroom_id=request.classroom_id,
            start_time=request.start_time,
            end_time=request.end_time,
            course_date=request.course_date
        )


class Reservations(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True)
    student_id = Column(String(50), ForeignKey('students.id'), nullable=False)
    schedule_id = Column(Integer, ForeignKey('schedules.id'), nullable=False)
    reservated_date = Column(Date, nullable=False)
    reservated_time = Column(Time, nullable=False)
    status = Column(String(20), nullable=False)
    notes = Column(String(255), nullable=True)

    students = relationship("Students", back_populates="reservations")
    schedules = relationship("Schedules", back_populates="reservations")

    @classmethod
    def create(cls, request: CreateReservationRequest) -> "Reservations":

        return cls(
            student_id=request.student_id,
            schedule_id=request.schedule_id,
            reservated_date=request.reservated_date,
            reservated_time=request.reservated_time,
            status=request.status,
            notes=request.notes
        )


class Payments(Base):
    __tablename__ = "payments"

    uid = Column(String(50), primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    amount = Column(Integer, nullable=False)
    status = Column(String(8), nullable=False)
    is_paid_ok = Column(Boolean, nullable=False)
    status = Column(String(20), nullable=False)
    student_id = Column(String(50), ForeignKey('students.id'), nullable=False)

    students = relationship("Students", back_populates="payments")

    @classmethod
    def create(cls, request: CreateReservationRequest) -> "Reservations":

        return cls(
            uid=request.uid,
            name=request.name,
            amount=request.amount,
            status=request.status,
            is_paid_ok=request.is_paid_ok,
            student_id=request.student_id
        )
