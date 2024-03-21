from typing import List
from fastapi import Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from database.database_orm import Courses, Instructors, Students
from database.database import get_database
from schema.request import UpdateCourseRequest

class Repository:
    def __init__(self, session: Session = Depends(get_database)):
        self.session = session


class StudentRepository(Repository):

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
        

class InstructorRepository(Repository):


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


class CoursesRepository(Repository):


    def get_all_courses(self):
        results = self.session.execute(
            select(Courses, Instructors.name, Instructors.contact, Instructors.email)
            .join(Instructors, Instructors.id == Courses.instructor_id)
        ).all()


        courses_list = []
        for course, instructor_name, instructor_contact, instructor_email in results:

            course.instructor_name = instructor_name
            course.instructor_contact = instructor_contact
            course.instructor_email = instructor_email
            courses_list.append(course)

        return courses_list
    
    def get_course_by_id(self, id: int) -> Courses | None:
        result = self.session.execute(
            select(Courses, Instructors.name, Instructors.contact, Instructors.email)
            .join(Instructors, Instructors.id == Courses.instructor_id)
            .where(Courses.id == id)
        ).first()

        if result is None:
            raise HTTPException(status_code=404, detail="Course Not Found")

        course, instructor_name, instructor_contact, instructor_email = result
        course.instructor_name = instructor_name
        course.instructor_contact = instructor_contact
        course.instructor_email = instructor_email

        return course
    
    def create_course(self, course: Courses) -> Courses:
        try:
            self.session.add(instance=course)
            self.session.commit()
            self.session.refresh(instance=course)
            return course
        except IntegrityError as e:
            raise HTTPException(status_code=409, detail="ID already exist.")
        
    def update_course_by_id(self, id: int, request: UpdateCourseRequest):

        course = self.session.execute(select(Courses).filter_by(id=id)).scalar_one()
        if course:
            course.name = request.name
            course.description = request.description
            course.start_date = request.start_date
            course.end_date = request.end_date
            course.instructor_id = request.instructor_id

            self.session.commit()
            self.session.refresh(instance=course)

        else:
            raise HTTPException(status_code=404, detail="Course Not Found")

    def delete_course(self, id: int):
        self.session.execute(delete(Courses).where(Courses.id == id))
        self.session.commit()

class ClassroomsRepository(Repository):
    pass


class SchedulesRepository(Repository):
    pass


class ReservationRepository(Repository):
    pass