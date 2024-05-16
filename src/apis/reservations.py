from fastapi import APIRouter, Depends, HTTPException

from database.ReservationRepository import ReservationRepository
from schema.request import CreateReservationRequest, UpdateReservationRequest
from schema.response import ReservationSchema
from database.database_orm import Reservations
from functions.security import get_access_token
from functions.student import StudentFunction


router = APIRouter(prefix="/reservations")


@router.get("/", status_code=200, tags=["Reservations"])
def get_reservations_handler(
    _: str = Depends(get_access_token),
    repo: ReservationRepository = Depends()
):
    return repo.get_all_entities()


@router.get("/{id}", status_code=200, tags=["Reservations"])
def get_reservation_by_id_handler(
    id: int,
    _: str = Depends(get_access_token),
    repo: ReservationRepository = Depends()
):
    reservation = repo.get_entity_by_id(id=id)

    if reservation:
        return reservation

    raise HTTPException(
        status_code=404, detail=f"Not found reservation infomation of id = {id}")


@router.post("/", status_code=201, tags=["Reservations"])
def post_create_reservation_handler(
    request: CreateReservationRequest,
    access_token: str = Depends(get_access_token),
    student_func: StudentFunction = Depends(),
    repo: ReservationRepository = Depends()
) -> ReservationSchema:

    payload = student_func.decode_jwt(access_token=access_token)
    role = payload['role']

    if role == 'instructor':
        raise HTTPException(
            status_code=401, detail=f"Instructor can't add reservation.")

    reservation: Reservations = Reservations.create(request=request)
    reservation: Reservations = repo.create_entity(reservation=reservation)
    return ReservationSchema.from_orm(reservation)


@router.patch("/{id}", status_code=200, tags=["Reservations"])
def patch_update_reservation_by_id_handler(
    id: int,
    request: UpdateReservationRequest,
    access_token: str = Depends(get_access_token),
    student_func: StudentFunction = Depends(),
    repo: ReservationRepository = Depends()
):

    payload = student_func.decode_jwt(access_token=access_token)
    role = payload['role']

    if role == 'instructor':
        raise HTTPException(
            status_code=401, detail=f"Instructor can't edit reservation.")

    reservation = repo.get_entity_by_id(id=id)

    if reservation:
        repo.update_entity_by_id(id=id, request=request)
    else:
        raise HTTPException(status_code=404, detail="Reservation Not Found")


@router.delete("/{id}", status_code=204, tags=["Reservations"])
def delete_reservation_handler(
    id: int,
    access_token: str = Depends(get_access_token),
    student_func: StudentFunction = Depends(),
    repo: ReservationRepository = Depends()
):

    payload = student_func.decode_jwt(access_token=access_token)
    role = payload['role']

    if role == 'instructor':
        raise HTTPException(
            status_code=401, detail=f"Instructor can't delete reservation.")

    reservation = repo.get_entity_by_id(id=id)

    if reservation:
        repo.delete_entity_by_id(id=id)
    else:
        raise HTTPException(status_code=404, detail="Reservation Not Found")
