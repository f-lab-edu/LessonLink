from abstract.repository import Repository
from database.database_orm import Schedules
from schema.request import UpdateScheduleRequest


from fastapi import HTTPException
from sqlalchemy import delete, select


from typing import List


class SchedulesRepository(Repository):

    def get_all_entities(self) -> List[Schedules]:
        return list(self.session.scalars(select(Schedules)))

    def get_entity_by_id(self, id: int) -> Schedules | None:
        return self.session.scalar(select(Schedules).where(Schedules.id == id))

    def create_entity(self, schedule: Schedules) -> Schedules:

        self.session.add(instance=schedule)
        self.session.commit()
        self.session.refresh(instance=schedule)
        return schedule

    def update_entity_by_id(self, id: int, request: UpdateScheduleRequest) -> None:
        schedule = self.session.execute(
            select(Schedules).filter_by(id=id)).scalar_one()
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

    def delete_entity_by_id(self, id: int) -> None:
        self.session.execute(delete(Schedules).where(Schedules.id == id))
        self.session.commit()
