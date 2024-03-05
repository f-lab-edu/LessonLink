from sqlalchemy import Column, String, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Students(Base):
    __tablename__ = "students"

    student_id = Column(String(50), primary_key=True)
    student_pw = Column(String(50))
    student_name = Column(String(20))
    student_contact = Column(String(20))
    student_email = Column(String(50))
    student_birth_date = Column(Date)
    student_gender = Column(String(5))
    join_date = Column(Date)

    def __repr__(self):
        return f"Students(student_id={self.student_id}, student_pw={self.student_pw}, student_name={self.student_name}, student_contact={self.student_contact}, student_email={self.student_email}, student_birth_date={self.student_birth_date}, student_gender={self.student_gender}, join_date={self.join_date})" 