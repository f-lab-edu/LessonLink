from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import delete, select, update

from database.database import get_database
from database.database_orm import Instructors
from schema.request import CreateInstructorRequest
from database.database_repo import InstructorRepository
from schema.response import InstructorSchema

router = APIRouter(prefix="/instructors")

@router.get("/", status_code=200, tags=["Instructors"])
def get_instructor_handler(repo: InstructorRepository = Depends()):
    return repo.get_all_instructors()

@router.get("/{instructor_id}", status_code=200, tags=["Instructors"])
def get_instructor_by_id_handler(
    instructor_id: str,
    repo: InstructorRepository = Depends()
):
    instructor = repo.get_instructor_by_id(instructor_id=instructor_id)
    
    if instructor_id:
        return instructor
    raise HTTPException(status_code=404, detail=f"Not found student infomation of id = {instructor_id}")

@router.post("/", status_code=201, tags=["Instructors"])
def post_create_instructor_handler(
    request: CreateInstructorRequest,
    repo: InstructorRepository = Depends()
):
    instructor: Instructors = Instructors.create(request=request)
    instructor: Instructors = repo.create_instructor(instructor=instructor)
    return InstructorSchema.from_orm(instructor)
    
@router.patch("/{instructor_id}", status_code=200, tags=["Instructors"])
def patch_update_instructor_pw_by_id_handler(
    instructor_id: str,
    instructor_pw: str,
    repo: InstructorRepository = Depends()
):
    instructor = repo.get_instructor_by_id(instructor_id=instructor_id)

    if instructor:
        repo.update_instructor_pw_by_id(instructor_id=instructor_id, instructor_pw=instructor_pw)
    else:
        raise HTTPException(status_code=404, detail="Instructor Not Found")
    
@router.delete("/{instructor_id}", status_code=204, tags=["Instructors"])
def delete_instructor_handler(
    instructor_id: str,
    repo: InstructorRepository = Depends()
):
    instructor = repo.get_instructor_by_id(instructor_id=instructor_id)

    if instructor:
        repo.delete_instructor(instructor_id=instructor_id)
    else:
        raise HTTPException(status_code=404, detail="Instructor Not Found")