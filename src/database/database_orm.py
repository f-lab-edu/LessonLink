from sqlalchemy import Column, String, Date, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

from schema.request import CreateCourseRequest, CreateInstructorRequest, CreateStudentRequest

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
            id = request.id,
            pw = encrypted_pw.decode(),
            name = request.name,
            contact = request.contact,
            email = request.email,
            birth_date = request.birth_date,
            gender = request.gender,
            join_date = request.join_date
        )
    
class Instructors(Base):
    __tablename__ = "instructors"

    courses = relationship("Courses", back_populates="instructors")

    id: Column = Column(String(50), primary_key=True)
    pw: Column = Column(String(255))
    name: Column = Column(String(20))
    contact: Column = Column(String(20))
    email: Column = Column(String(50))

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
            id = request.id,
            pw = encrypted_pw,
            name = request.name,
            contact = request.contact,
            email = request.email,
        )
    

class Courses(Base):
    __tablename__ = "courses"

    instructors = relationship("Instructors", back_populates="courses")

    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    description = Column(String(256))
    start_date = Column(Date)
    end_date = Column(Date)
    instructor_id = Column(String(50), ForeignKey('instructors.id'))

    @classmethod
    def create(cls, request: CreateCourseRequest) -> "Courses":

        return cls(
            id = request.id,
            name = request.name,
            description = request.description,
            start_date = request.start_date,
            end_date = request.end_date,
            instructor_id = request.instructor_id
        )