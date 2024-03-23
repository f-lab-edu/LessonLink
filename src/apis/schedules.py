from fastapi import APIRouter, Depends, HTTPException

from database.database_repo import SchedulesRepository
from schema.request import CreateScheduleRequest, UpdateScheduleRequest
from schema.response import ScheduleSchema
from database.database_orm import Schedules


router = APIRouter(prefix="/schedules")


@router.get("/", status_code=200, tags=["Schedules"])
def get_Schedules_handler(repo: SchedulesRepository = Depends()):
    return repo.get_all_schedules()

@router.get("/{id}", status_code=200, tags=["Schedules"])
def get_schedule_by_id_handler(
    id: int,
    repo: SchedulesRepository = Depends()
):
    schedule = repo.get_schedule_by_id(id=id)

    if schedule:
        return schedule
    
    raise HTTPException(status_code=404, detail=f"Not found schedule infomation of id = {id}")

@router.post("/", status_code=201, tags=["Schedules"])
def post_create_id_handler(
    request: CreateScheduleRequest,
    repo: SchedulesRepository = Depends()
) -> ScheduleSchema:
    schedule: Schedules = Schedules.create(request=request)
    schedule: Schedules = repo.create_schedule(schedule=schedule)
    return ScheduleSchema.from_orm(schedule)
    
@router.patch("/{id}", status_code=200, tags=["Schedules"])
def patch_update_schedule_pw_by_id_handler(
    id: int,
    request: UpdateScheduleRequest,
    repo: SchedulesRepository = Depends()
):
    schedule = repo.get_schedule_by_id(id=id)

    if schedule:
        repo.update_schedule_by_id(id=id, request=request)
    else:
        raise HTTPException(status_code=404, detail="Schedule Not Found")
    
@router.delete("/{id}", status_code=204, tags=["Schedules"])
def delete_schedule_handler(
    id: int,
    repo: SchedulesRepository = Depends()
):
    schedule = repo.get_schedule_by_id(id=id)

    if schedule:
        repo.delete_schedule(id=id)
    else:
        raise HTTPException(status_code=404, detail="Schedule Not Found")