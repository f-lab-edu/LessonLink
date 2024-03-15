from typing import List
from fastapi import Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from database.database_orm import Courses, Instructors, Students
from database.database import get_database


class StudentRepository:
    def __init__(self, session: Session = Depends(get_database)):
        self.session = session

    def get_all_students(self) -> List[Students]:
        return list(self.session.scalars(select(Students)))
    
    def get_student_by_id(self, id) -> Students | None:
        return self.session.scalar(select(Students).where(Students.id == id))
    
    def create_student(self, student: Students) -> Students:
        try:
            self.session.add(instance=student)
            self.session.commit()
            self.session.refresh(instance=student)
            return student
        except IntegrityError as e:
            raise HTTPException(status_code=409, detail="ID already exist.")
        
    def update_student_pw_by_id(self, id: str, pw: str):
        student = self.session.execute(select(Students).filter_by(id=id)).scalar_one()
        student.pw = pw
        self.session.commit()
        self.session.refresh(instance=student)

    def delete_student(self, id: str):
        self.session.execute(delete(Students).where(Students.id == id))
        self.session.commit()
        

class InstructorRepository:
    def __init__(self, session: Session = Depends(get_database)):
        self.session = session

    def get_all_instructors(self) -> List[Instructors]:
        return list(self.session.scalars(select(Instructors)))
    
    def get_instructor_by_id(self, id: str) -> Instructors | None:
        return self.session.scalar(select(Instructors).where(Instructors.id == id))
    
    def create_instructor(self, instructor: Instructors) -> Instructors:
        try:
            self.session.add(instance=instructor)
            self.session.commit()
            self.session.refresh(instance=instructor)
            return instructor
        except IntegrityError as e:
            raise HTTPException(status_code=409, detail="ID already exist.")
        
    def update_instructor_pw_by_id(self, id: str, pw: str):
        instructor = self.session.execute(select(Instructors).filter_by(id=id)).scalar_one()
        instructor.pw = pw
        self.session.commit()
        self.session.refresh(instance=instructor)

    def delete_instructor(self, id: str):
        self.session.execute(delete(Instructors).where(Instructors.id == id))
        self.session.commit()


class CoursesRepository:
    def __init__(self, session: Session = Depends(get_database)):
        self.session = session

    def get_all_courses(self) -> List[Courses]:
        return list(self.session.scalars(select(Courses)))
    
    def get_course_by_id(self, id: int) -> Courses | None:
        return self.session.scalar(select(Courses).where(Courses.id == id))
    
    def create_course(self, course: Courses) -> Courses:
        try:
            self.session.add(instance=course)
            self.session.commit()
            self.session.refresh(instance=course)
            return course
        except IntegrityError as e:
            raise HTTPException(status_code=409, detail="ID already exist.")
        
    # def update_course_by_id(self, id: int):
    #     pass
