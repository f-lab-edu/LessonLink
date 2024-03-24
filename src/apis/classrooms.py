from fastapi import APIRouter, Depends, HTTPException

from database.database_repo import ClassroomsRepository
from schema.request import CreateClassroomRequest, UpdateClassroomRequest
from database.database_orm import Classrooms
from schema.response import ClassroomSchema


router = APIRouter(prefix="/classrooms")


@router.get("/", status_code=200, tags=["Classrooms"])
def get_classroom_handler(repo: ClassroomsRepository = Depends()):
    return repo.get_all_entities()


@router.get("/{id}", status_code=200, tags=["Classrooms"])
def get_classroom_by_id_handler(
    id: int,
    repo: ClassroomsRepository = Depends()
):
    classroom = repo.get_entity_by_id(id=id)

    if classroom:
        return classroom

    raise HTTPException(
        status_code=404, detail=f"Not found classroom infomation of id = {id}")


@router.post("/", status_code=201, tags=["Classrooms"])
def post_create_classroom_handler(
    request: CreateClassroomRequest,
    repo: ClassroomsRepository = Depends()
):
    classroom: Classrooms = Classrooms.create(request=request)
    classroom: Classrooms = repo.create_entity(classroom=classroom)
    return ClassroomSchema.from_orm(classroom)


@router.patch("/{id}", status_code=200, tags=["Classrooms"])
def patch_classroom_handler(
    id: int,
    request: UpdateClassroomRequest,
    repo: ClassroomsRepository = Depends()
):
    classroom = repo.get_entity_by_id(id=id)

    if classroom:
        repo.update_entity_by_id(id=id, request=request)
    else:
        raise HTTPException(status_code=404, detail="Classroom Not Found")


@router.delete("/{id}", status_code=204, tags=["Classrooms"])
def delete_classroom_handler(
    id: int,
    repo: ClassroomsRepository = Depends()
):
    classroom = repo.get_entity_by_id(id=id)

    if classroom:
        repo.delete_entity_by_id(id=id)
    else:
        raise HTTPException(status_code=404, detail="Classroom Not Found")
