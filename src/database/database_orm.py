from sqlalchemy import Column, String, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Students(Base):
    __tablename__ = "students"

    student_id: Column = Column(String(50), primary_key=True)
    student_pw: Column = Column(String(50))
    student_name: Column = Column(String(20))
    student_contact: Column = Column(String(20))
    student_email: Column = Column(String(50))
    student_birth_date: Column = Column(Date)
    student_gender: Column = Column(String(5))
    join_date: Column = Column(Date)

    def __repr__(self):
        return "".join((
            f"Students(",
            f"student_id={self.student_id!r}, ",
            f"student_pw={self.student_pw!r}, ",
            f"student_contact={self.student_contact!r}, ",
            f"student_email={self.student_email}, ",
            f"student_birth_date={self.student_birth_date!r}, ",
            f"student_gender={self.student_gender!r}, ",
            f"join_date={self.join_date!r}",
            f")"
        ))
    
class Instructors(Base):
    __tablename__ = "instructors"

    instructor_id: Column = Column(String(50), primary_key=True)
    instructor_pw: Column = Column(String(50))
    instructor_name: Column = Column(String(20))
    instructor_contact: Column = Column(String(20))
    instructor_email: Column = Column(String(20))
    subject: Column = Column(String(20))


    def __repr__(self):
        return "".join((
            f"Instructors(",
            f"instructor_id={self.instructor_id!r}, ",
            f"instructor_pw={self.instructor_pw!r}, ",
            f"instructor_name={self.instructor_name!r}, ",
            f"instructor_contact={self.instructor_contact}, ",
            f"instructor_email={self.instructor_email!r}, ",
            f"subject={self.subject!r}, ",
            f")"
        ))