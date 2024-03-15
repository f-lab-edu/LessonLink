from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, select, update

from database.database import get_database
from database.database_orm import Students
from schema.request import CreateStudentRequest
from database.database_repo import StudentRepository
from schema.response import StudentSchema

router = APIRouter(prefix="/students")

@router.get("/", status_code=200, tags=["Students"])
def get_students_handler(repo: StudentRepository = Depends()):
    return repo.get_all_students()

@router.get("/{student_id}", status_code=200, tags=["Students"])
def get_students_by_id_handler(
    student_id: str,
    repo: StudentRepository = Depends()
):
    student = repo.get_student_by_id(id=student_id)
    
    if student:
        return student
    raise HTTPException(status_code=404, detail=f"Not found student infomation of id = {student_id}")

@router.post("/", status_code=201, tags=["Students"])
def post_create_student_id_handler(
    request: CreateStudentRequest,
    repo: StudentRepository = Depends()
) -> StudentSchema:
    student: Students = Students.create(request=request)
    student: Students = repo.create_student(student=student)
    return StudentSchema.from_orm(student)
    
@router.patch("/{student_id}", status_code=200, tags=["Students"])
def patch_update_student_pw_by_id_handler(
    student_id: str,
    student_pw: str,
    repo: StudentRepository = Depends()
):
    student = repo.get_student_by_id(student_id=student_id)

    if student:
        repo.update_student_pw_by_id(student_id=student_id, student_pw=student_pw)
    else:
        raise HTTPException(status_code=404, detail="Student Not Found")
    
@router.delete("/{student_id}", status_code=204, tags=["Students"])
def delete_student_handler(
    student_id: str,
    repo: StudentRepository = Depends()
):
    student = repo.get_student_by_id(student_id=student_id)

    if student:
        repo.delete_student(student_id=student_id)
    else:
        raise HTTPException(status_code=404, detail="Student Not Found")