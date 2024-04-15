from abstract.repository import Repository
from database.database_orm import Reservations
from schema.request import UpdateReservationRequest


from fastapi import HTTPException
from sqlalchemy import delete, select


from typing import List


class ReservationRepository(Repository):

    def get_all_entities(self) -> List[Reservations]:
        return list(self.session.scalars(select(Reservations)))

    def get_entity_by_id(self, id: int) -> Reservations | None:
        return self.session.scalar(select(Reservations).where(Reservations.id == id))

    def create_entity(self, reservation: Reservations) -> Reservations:
        self.session.add(instance=reservation)
        self.session.commit()
        self.session.refresh(instance=reservation)
        return reservation

    def update_entity_by_id(self, id: int, request: UpdateReservationRequest) -> None:
        reservation = self.session.execute(
            select(Reservations).filter_by(id=id)).scalar_one()
        if reservation:
            reservation.student_id = request.student_id
            reservation.schedule_id = request.schedule_id
            reservation.reservated_date = request.reservated_date
            reservation.reservated_time = request.reservated_time
            reservation.status = request.status
            reservation.notes = request.notes

            self.session.commit()
            self.session.refresh(instance=reservation)

        else:
            raise HTTPException(
                status_code=404, detail="Reservation Not Found")

    def delete_entity_by_id(self, id: int) -> None:
        self.session.execute(delete(Reservations).where(Reservations.id == id))
        self.session.commit()
