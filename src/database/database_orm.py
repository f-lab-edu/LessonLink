from sqlalchemy import Column, String, Date, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

from schema.request import CreateInstructorRequest, CreateStudentRequest

Base = declarative_base()


class Students(Base):
    __tablename__ = "students"

    id: Column = Column(String(50), primary_key=True)
    pw: Column = Column(String(50))
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
        return cls(
            id = request.id,
            pw = request.pw,
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

    instructor_id: Column = Column(String(50), primary_key=True)
    instructor_pw: Column = Column(String(50))
    instructor_name: Column = Column(String(20))
    instructor_contact: Column = Column(String(20))
    instructor_email: Column = Column(String(20))

    def __repr__(self):
        return "".join((
            f"Instructors(",
            f"instructor_id={self.instructor_id!r}, ",
            f"instructor_pw={self.instructor_pw!r}, ",
            f"instructor_name={self.instructor_name!r}, ",
            f"instructor_contact={self.instructor_contact}, ",
            f"instructor_email={self.instructor_email!r}, ",
            f")"
        ))
    
    @classmethod
    def create(cls, request: CreateInstructorRequest) -> "Instructors":
        return cls(
            instructor_id = request.instructor_id,
            instructor_pw = request.instructor_pw,
            instructor_name = request.instructor_name,
            instructor_contact = request.instructor_contact,
            instructor_email = request.instructor_email,
        )
    

class Courses(Base):
    __tablename__ = "courses"

    instructors = relationship("Instructors", back_populates="courses")

    course_id = Column(Integer, primary_key=True)
    course_name = Column(String(20))
    course_description = Column(String(256))
    course_start_date = Column(Date)
    course_end_date = Column(Date)
    instructor_id = Column(String(50), ForeignKey('instructors.instructor_id'))

