from abstract.repository import Repository
from database.database_orm import Courses, Instructors
from schema.request import UpdateCourseRequest


from fastapi import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError


class CoursesRepository(Repository):
    def get_all_entities(self):
        results = self.session.execute(
            select(Courses, Instructors.name,
                   Instructors.contact, Instructors.email)
            .join(Instructors, Instructors.id == Courses.instructor_id)
        ).all()

        courses_list = []
        for course, instructor_name, instructor_contact, instructor_email in results:

            course.instructor_name = instructor_name
            course.instructor_contact = instructor_contact
            course.instructor_email = instructor_email
            courses_list.append(course)

        return courses_list

    def get_entity_by_id(self, id: int) -> Courses | None:

        result = self.session.execute(
            select(Courses, Instructors.name,
                   Instructors.contact, Instructors.email)
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

    def create_entity(self, course: Courses) -> Courses:
        try:
            self.session.add(instance=course)
            self.session.commit()
            self.session.refresh(instance=course)
            return course
        except IntegrityError as e:
            raise HTTPException(status_code=409, detail="ID already exist.")

    def update_entity_by_id(self, id: int, request: UpdateCourseRequest) -> None:

        course = self.session.execute(
            select(Courses).filter_by(id=id)).scalar_one()
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

    def delete_entity_by_id(self, id: int) -> None:
        self.session.execute(delete(Courses).where(Courses.id == id))
        self.session.commit()
