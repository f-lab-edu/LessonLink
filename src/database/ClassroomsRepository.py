from abstract.repository import Repository
from database.database_orm import Classrooms
from schema.request import UpdateClassroomRequest


from fastapi import HTTPException
from sqlalchemy import delete, select


from typing import List


class ClassroomsRepository(Repository):

    def get_all_entities(self) -> List[Classrooms]:
        return list(self.session.scalars(select(Classrooms)))

    def get_entity_by_id(self, id: int) -> Classrooms | None:
        return self.session.scalar(select(Classrooms).where(Classrooms.id == id))

    def create_entity(self, classroom: Classrooms) -> Classrooms:
        self.session.add(instance=classroom)
        self.session.commit()
        self.session.refresh(instance=classroom)
        return classroom

    def update_entity_by_id(self, id: int, request: UpdateClassroomRequest) -> None:

        classroom = self.session.execute(
            select(Classrooms).filter_by(id=id)).scalar_one()
        if classroom:
            classroom.name = request.name
            classroom.location = request.location
            classroom.capacity = request.capacity
            classroom.building_name = request.building_name

            self.session.commit()
            self.session.refresh(instance=classroom)

        else:
            raise HTTPException(status_code=404, detail="Classroom Not Found")

    def delete_entity_by_id(self, id: int) -> None:
        self.session.execute(delete(Classrooms).where(Classrooms.id == id))
        self.session.commit()
