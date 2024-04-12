from fastapi import APIRouter, Depends, HTTPException

from database.SchedulesRepository import SchedulesRepository
from schema.request import CreateScheduleRequest, UpdateScheduleRequest
from schema.response import ScheduleSchema
from database.database_orm import Schedules
from functions.security import get_access_token
from functions.student import StudentFunction
from functions.instructor import InstructorFunction


router = APIRouter(prefix="/schedules")


@router.get("/", status_code=200, tags=["Schedules"])
def get_schedules_handler(
    access_token: str = Depends(get_access_token),
    student_func: StudentFunction = Depends(),
    repo: SchedulesRepository = Depends()
):
    return repo.get_all_entities()


@router.get("/{id}", status_code=200, tags=["Schedules"])
def get_schedule_by_id_handler(
    id: int,
    access_token: str = Depends(get_access_token),
    student_func: StudentFunction = Depends(),
    repo: SchedulesRepository = Depends()
):
    schedule = repo.get_entity_by_id(id=id)

    if schedule:
        return schedule

    raise HTTPException(
        status_code=404, detail=f"Not found schedule infomation of id = {id}")


@router.post("/", status_code=201, tags=["Schedules"])
def post_create_schedule_handler(
    request: CreateScheduleRequest,
    access_token: str = Depends(get_access_token),
    instructor_func: InstructorFunction = Depends(),
    repo: SchedulesRepository = Depends()
) -> ScheduleSchema:

    payload = instructor_func.decode_jwt(access_token=access_token)
    role = payload['role']

    if role == 'student':
        raise HTTPException(
            status_code=401, detail=f"Student can't add schedule.")

    schedule: Schedules = Schedules.create(request=request)
    schedule: Schedules = repo.create_entity(schedule=schedule)
    return ScheduleSchema.from_orm(schedule)


@router.patch("/{id}", status_code=200, tags=["Schedules"])
def patch_update_schedule_by_id_handler(
    id: int,
    request: UpdateScheduleRequest,
    access_token: str = Depends(get_access_token),
    instructor_func: InstructorFunction = Depends(),
    repo: SchedulesRepository = Depends()
):

    payload = instructor_func.decode_jwt(access_token=access_token)
    role = payload['role']

    if role == 'student':
        raise HTTPException(
            status_code=401, detail=f"Student can't edit schedule.")

    schedule = repo.get_entity_by_id(id=id)

    if schedule:
        repo.update_entity_by_id(id=id, request=request)
    else:
        raise HTTPException(status_code=404, detail="Schedule Not Found")


@router.delete("/{id}", status_code=204, tags=["Schedules"])
def delete_schedule_handler(
    id: int,
    access_token: str = Depends(get_access_token),
    instructor_func: InstructorFunction = Depends(),
    repo: SchedulesRepository = Depends()
):

    payload = instructor_func.decode_jwt(access_token=access_token)
    role = payload['role']

    if role == 'student':
        raise HTTPException(
            status_code=401, detail=f"Student can't delete schedule.")

    schedule = repo.get_entity_by_id(id=id)

    if schedule:
        repo.delete_entity_by_id(id=id)
    else:
        raise HTTPException(status_code=404, detail="Schedule Not Found")
