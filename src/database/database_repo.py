from typing import List
from fastapi import Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from database.database_orm import Classrooms, Courses, Instructors, Reservations, Schedules, Students
from database.database import get_database
from schema.request import UpdateClassroomRequest, UpdateCourseRequest, UpdateReservationRequest, UpdateScheduleRequest

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

    def get_all_classrooms(self) -> List[Classrooms]:
        return list(self.session.scalars(select(Classrooms)))

    def get_classroom_by_id(self, id: int) -> Classrooms | None:
        return self.session.scalar(select(Classrooms).where(Classrooms.id == id))

    def create_classrooms(self, classroom: Classrooms) -> Classrooms:
        self.session.add(instance=classroom)
        self.session.commit()
        self.session.refresh(instance=classroom)
        return classroom
    
    def update_classroom_by_id(self, id: int, request: UpdateClassroomRequest):
        classroom = self.session.execute(select(Classrooms).filter_by(id=id)).scalar_one()
        if classroom:
            classroom.name = request.name
            classroom.location = request.location
            classroom.capacity = request.capacity
            classroom.building_name = request.building_name

            self.session.commit()
            self.session.refresh(instance=classroom)

        else:
            raise HTTPException(status_code=404, detail="Classroom Not Found")
        
    def delete_classroom(self, id: int):
        self.session.execute(delete(Classrooms).where(Classrooms.id == id))
        self.session.commit()

class SchedulesRepository(Repository):
    
    def get_all_schedules(self) -> List[Schedules]:
        return list(self.session.scalars(select(Schedules)))


    def get_schedule_by_id(self, id: int) -> Schedules | None:
        return self.session.scalar(select(Schedules).where(Schedules.id == id))


    def create_schedule(self, schedule: Schedules) -> Schedules:

        self.session.add(instance=schedule)
        self.session.commit()
        self.session.refresh(instance=schedule)
        return schedule


    def update_schedule_by_id(self, id: int, request: UpdateScheduleRequest):
        schedule = self.session.execute(select(Schedules).filter_by(id=id)).scalar_one()
        if schedule:
            schedule.course_id = request.course_id
            schedule.classroom_id = request.classroom_id
            schedule.start_time = request.start_time
            schedule.end_time = request.end_time
            schedule.course_date = request.course_date

            self.session.commit()
            self.session.refresh(instance=schedule)

        else:
            raise HTTPException(status_code=404, detail="Schedule Not Found")


    def delete_schedule(self, id: int):
        self.session.execute(delete(Schedules).where(Schedules.id == id))
        self.session.commit()



class ReservationRepository(Repository):

    def get_all_reservations(self) -> List[Reservations]:
        return list(self.session.scalars(select(Reservations)))


    def get_reservation_by_id(self, id: int) -> Reservations | None:
        return self.session.scalar(select(Reservations).where(Reservations.id == id))


    def create_reservation(self, reservation: Reservations) -> Reservations:
        self.session.add(instance=reservation)
        self.session.commit()
        self.session.refresh(instance=reservation)
        return reservation


    def update_reservation_by_id(self, id: int, request: UpdateReservationRequest):
        reservation = self.session.execute(select(Reservations).filter_by(id=id)).scalar_one()
        if reservation:
            reservation.student_id = request.student_id
            reservation.course_id = request.course_id
            reservation.schedule_id = request.schedule_id
            reservation.reservated_date = request.reservated_date
            reservation.reservated_time = request.reservated_time
            reservation.status = request.status
            reservation.notes = request.notes

            self.session.commit()
            self.session.refresh(instance=reservation)

        else:
            raise HTTPException(status_code=404, detail="Reservation Not Found")


    def delete_reservation(self, id: int):
        self.session.execute(delete(Reservations).where(Reservations.id == id))
        self.session.commit()