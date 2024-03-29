import bcrypt
from fastapi import APIRouter, Depends, HTTPException

from database.database_orm import Instructors
from schema.request import CreateInstructorRequest, UpdatePasswordRequest
from database.database_repo import InstructorRepository
from schema.response import InstructorSchema

router = APIRouter(prefix="/instructors")


@router.get("/", status_code=200, tags=["Instructors"])
def get_instructor_handler(repo: InstructorRepository = Depends()):
    return repo.get_all_entities()


@router.get("/{id}", status_code=200, tags=["Instructors"])
def get_instructor_by_id_handler(
    id: str,
    repo: InstructorRepository = Depends()
):
    instructor = repo.get_entity_by_id(id=id)

    if id:
        return instructor
    raise HTTPException(
        status_code=404, detail=f"Not found instructor infomation of id = {id}")


@router.post("/", status_code=201, tags=["Instructors"])
def post_create_instructor_handler(
    request: CreateInstructorRequest,
    repo: InstructorRepository = Depends()
):
    instructor: Instructors = Instructors.create(request=request)
    instructor: Instructors = repo.create_entity(instructor=instructor)
    return InstructorSchema.from_orm(instructor)


@router.patch("/{id}", status_code=200, tags=["Instructors"])
def patch_update_instructor_pw_by_id_handler(
    id: str,
    request: UpdatePasswordRequest,
    repo: InstructorRepository = Depends()
):
    instructor = repo.get_entity_by_id(id=id)

    if instructor:
        encrypted_pw = bcrypt.hashpw(
            request.pw.encode(), salt=bcrypt.gensalt())
        repo.update_entity_by_id(id=id, pw=encrypted_pw)
    else:
        raise HTTPException(status_code=404, detail="Instructor Not Found")


@router.delete("/{id}", status_code=204, tags=["Instructors"])
def delete_instructor_handler(
    id: str,
    repo: InstructorRepository = Depends()
):
    instructor = repo.get_entity_by_id(id=id)

    if instructor:
        repo.delete_entity_by_id(id=id)
    else:
        raise HTTPException(status_code=404, detail="Instructor Not Found")
