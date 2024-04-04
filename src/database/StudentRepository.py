from abstract.repository import Repository
from database.database_orm import Students


from fastapi import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError


from typing import List


class StudentRepository(Repository):

    def get_all_entities(self) -> List[Students]:
        return list(self.session.scalars(select(Students)))

    def get_entity_by_id(self, id: str) -> Students | None:
        return self.session.scalar(select(Students)
                                   .where(Students.id == id))

    def create_entity(self, student: Students) -> Students:
        try:
            self.session.add(student)
            self.session.commit()
            self.session.refresh(student)
            return student
        except IntegrityError:
            raise HTTPException(status_code=409, detail="ID already exists.")

    def update_entity_by_id(self, id: str, pw: str) -> None:
        student = self.session.execute(select(Students)
                                       .filter_by(id=id)).scalar_one()
        student.pw = pw
        self.session.commit()
        self.session.refresh(student)

    def delete_entity_by_id(self, id: str) -> None:
        self.session.execute(delete(Students)
                             .where(Students.id == id))
        self.session.commit()
