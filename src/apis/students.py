from fastapi import APIRouter, Depends, HTTPException

from database.database_orm import Students
from schema.request import CreateStudentRequest, UpdatePasswordRequest
from database.database_repo import StudentRepository
from schema.response import StudentSchema

import bcrypt

router = APIRouter(prefix="/students")

@router.get("/", status_code=200, tags=["Students"])
def get_students_handler(repo: StudentRepository = Depends()):
    return repo.get_all_students()

@router.get("/{id}", status_code=200, tags=["Students"])
def get_student_by_id_handler(
    id: str,
    repo: StudentRepository = Depends()
):
    student = repo.get_student_by_id(id=id)
    
    if student:
        return student
    raise HTTPException(status_code=404, detail=f"Not found student infomation of id = {id}")

@router.post("/", status_code=201, tags=["Students"])
def post_create_id_handler(
    request: CreateStudentRequest,
    repo: StudentRepository = Depends()
) -> StudentSchema:
    student: Students = Students.create(request=request)
    student: Students = repo.create_student(student=student)
    return StudentSchema.from_orm(student)
    
@router.patch("/{id}", status_code=200, tags=["Students"])
def patch_update_student_pw_by_id_handler(
    id: str,
    request: UpdatePasswordRequest,
    repo: StudentRepository = Depends()
):
    student = repo.get_student_by_id(id=id)

    if student:
        encrypted_pw = bcrypt.hashpw(request.pw.encode(), salt=bcrypt.gensalt())
        repo.update_student_pw_by_id(id=id, pw=encrypted_pw)
    else:
        raise HTTPException(status_code=404, detail="Student Not Found")
    
@router.delete("/{id}", status_code=204, tags=["Students"])
def delete_student_handler(
    id: str,
    repo: StudentRepository = Depends()
):
    student = repo.get_student_by_id(id=id)

    if student:
        repo.delete_student(id=id)
    else:
        raise HTTPException(status_code=404, detail="Student Not Found")