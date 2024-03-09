from typing import List
from fastapi import Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from database.database_orm import Instructors, Students
from database.database import get_database

class StudentRepository:
    def __init__(self, session: Session = Depends(get_database)):
        self.session = session

    def get_all_students(self) -> List[Students]:
        return list(self.session.scalars(select(Students)))
    
    def get_student_by_id(self, student_id) -> Students | None:
        return self.session.scalar(select(Students).where(Students.student_id == student_id))
    
    def create_student(self, student: Students) -> Students:
        try:
            self.session.add(instance=student)
            self.session.commit()
            self.session.refresh(instance=student)
            return student
        except IntegrityError as e:
            raise HTTPException(status_code=409, detail="ID already exist.")
        
    def update_student_pw_by_id(self, student_id: str, student_pw: str):
        student = self.session.execute(select(Students).filter_by(student_id=student_id)).scalar_one()
        student.student_pw = student_pw
        self.session.commit()
        self.session.refresh(instance=student)

    def delete_student(self, student_id: str):
        self.session.execute(delete(Students).where(Students.student_id == student_id))
        self.session.commit()
        
class InstructorRepository:
    def __init__(self, session: Session = Depends(get_database)):
        self.session = session

    def get_all_instructors(self) -> List[Instructors]:
        return list(self.session.scalars(select(Instructors)))
    
    def get_instructor_by_id(self, instructor_id: str) -> Instructors | None:
        return self.session.scalar(select(Instructors).where(Instructors.instructor_id == instructor_id))
    
    def create_instructor(self, instructor: Instructors) -> Instructors:
        try:
            self.session.add(instance=instructor)
            self.session.commit()
            self.session.refresh(instance=instructor)
            return instructor
        except IntegrityError as e:
            raise HTTPException(status_code=409, detail="ID already exist.")
        
    def update_instructor_pw_by_id(self, instructor_id: str, instructor_pw: str):
        instructor = self.session.execute(select(Instructors).filter_by(instructor_id=instructor_id)).scalar_one()
        instructor.instructor_pw = instructor_pw
        self.session.commit()
        self.session.refresh(instance=instructor)

    def delete_instructor(self, instructor_id: str):
        self.session.execute(delete(Instructors).where(Instructors.instructor_id == instructor_id))
        self.session.commit()