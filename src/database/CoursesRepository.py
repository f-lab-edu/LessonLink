from abstract.repository import Repository, RepositoryAsync
from database.database_orm import Courses, Instructors
from schema.request import UpdateCourseRequest


from fastapi import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError


class CoursesRepository(RepositoryAsync):
    async def get_all_entities(self):
        results = await self.session.execute(
            select(Courses, Instructors.name,
                   Instructors.contact, Instructors.email)
            .join(Instructors, Instructors.id == Courses.instructor_id)
        )

        scalars = results.scalars()

        return scalars.all()

    async def get_entity_by_id(self, id: int) -> Courses | None:

        result = await self.session.execute(
            select(Courses, Instructors.name,
                   Instructors.contact, Instructors.email)
            .join(Instructors, Instructors.id == Courses.instructor_id)
            .where(Courses.id == id)
        )

        first_result = result.scalar()

        if first_result is None:
            raise HTTPException(status_code=404, detail="Course Not Found")

        return first_result

    async def create_entity(self, course: Courses) -> Courses:
        try:
            self.session.add(instance=course)
            await self.session.commit()
            await self.session.refresh(instance=course)
            return course
        except IntegrityError as e:
            raise HTTPException(status_code=409, detail="ID already exist.")

    async def update_entity_by_id(self, id: int, request: UpdateCourseRequest) -> None:

        course = await self.session.execute(
            select(Courses).filter_by(id=id))
        
        scalar_one = course.scalar_one()

        if scalar_one:
            scalar_one.name = request.name
            scalar_one.description = request.description
            scalar_one.start_date = request.start_date
            scalar_one.end_date = request.end_date
            scalar_one.instructor_id = request.instructor_id

            await self.session.commit()
            await self.session.refresh(instance=scalar_one)

        else:
            raise HTTPException(status_code=404, detail="Course Not Found")

    async def delete_entity_by_id(self, id: int) -> None:
        await self.session.execute(delete(Courses).where(Courses.id == id))
        await self.session.commit()
