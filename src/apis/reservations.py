from fastapi import APIRouter, Depends, HTTPException

from database.database_repo import ReservationRepository
from schema.request import CreateReservationRequest, UpdateReservationRequest
from schema.response import ReservationSchema
from database.database_orm import Reservations


router = APIRouter(prefix="/reservations")


@router.get("/", status_code=200, tags=["Reservations"])
def get_Reservations_handler(repo: ReservationRepository = Depends()):
    return repo.get_all_reservations()

@router.get("/{id}", status_code=200, tags=["Reservations"])
def get_reservation_by_id_handler(
    id: int,
    repo: ReservationRepository = Depends()
):
    reservation = repo.get_reservation_by_id(id=id)

    if reservation:
        return reservation
    
    raise HTTPException(status_code=404, detail=f"Not found reservation infomation of id = {id}")

@router.post("/", status_code=201, tags=["Reservations"])
def post_create_id_handler(
    request: CreateReservationRequest,
    repo: ReservationRepository = Depends()
) -> ReservationSchema:
    reservation: Reservations = Reservations.create(request=request)
    reservation: Reservations = repo.create_reservation(reservation=reservation)
    return ReservationSchema.from_orm(reservation)
    
@router.patch("/{id}", status_code=200, tags=["Reservations"])
def patch_update_reservation_pw_by_id_handler(
    id: int,
    request: UpdateReservationRequest,
    repo: ReservationRepository = Depends()
):
    reservation = repo.get_reservation_by_id(id=id)

    if reservation:
        repo.update_reservation_by_id(id=id, request=request)
    else:
        raise HTTPException(status_code=404, detail="Reservation Not Found")
    
@router.delete("/{id}", status_code=204, tags=["Reservations"])
def delete_reservation_handler(
    id: int,
    repo: ReservationRepository = Depends()
):
    reservation = repo.get_reservation_by_id(id=id)

    if reservation:
        repo.delete_reservation(id=id)
    else:
        raise HTTPException(status_code=404, detail="Reservation Not Found")