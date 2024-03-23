from fastapi import APIRouter, Depends, HTTPException

from database.database_repo import ReservationRepository
from schema.request import CreateReservationRequest, UpdateReservationRequest
from schema.response import ReservationSchema


router = APIRouter(prefix="/reservations")


@router.get("/", status_code=200, tags=["Reservations"])
def get_Reservations_handler(repo: ReservationRepository = Depends()):
    pass

@router.get("/{id}", status_code=200, tags=["Reservations"])
def get_reservation_by_id_handler(
    id: int,
    repo: ReservationRepository = Depends()
):
    pass

@router.post("/", status_code=201, tags=["Reservations"])
def post_create_id_handler(
    request: CreateReservationRequest,
    repo: ReservationRepository = Depends()
) -> ReservationSchema:
    pass
    
@router.patch("/{id}", status_code=200, tags=["Reservations"])
def patch_update_reservation_pw_by_id_handler(
    id: int,
    request: UpdateReservationRequest,
    repo: ReservationRepository = Depends()
):
    pass
    
@router.delete("/{id}", status_code=204, tags=["Reservations"])
def delete_reservation_handler(
    id: int,
    repo: ReservationRepository = Depends()
):
    pass