from abstract.repository import Repository
from database.database_orm import Instructors


from fastapi import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError


from typing import List


class InstructorRepository(Repository):

    def get_all_entities(self) -> List[Instructors]:
        return list(self.session.scalars(select(Instructors)))

    def get_entity_by_id(self, id: str) -> Instructors | None:
        return self.session.scalar(select(Instructors)
                                   .where(Instructors.id == id))

    def create_entity(self, instructor: Instructors) -> Instructors:
        try:
            self.session.add(instance=instructor)
            self.session.commit()
            self.session.refresh(instance=instructor)
            return instructor
        except IntegrityError as e:
            raise HTTPException(status_code=409, detail="ID already exist.")

    def update_entity_by_id(self, id: str, pw: str) -> None:
        instructor = self.session.execute(select(Instructors)
                                          .filter_by(id=id)).scalar_one()
        instructor.pw = pw
        self.session.commit()
        self.session.refresh(instance=instructor)

    def delete_entity_by_id(self, id: str) -> None:
        self.session.execute(delete(Instructors).where(Instructors.id == id))
        self.session.commit()
