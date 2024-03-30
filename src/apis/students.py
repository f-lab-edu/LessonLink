from fastapi import APIRouter, Depends, HTTPException

from database.database_orm import Students
from database.database_repo import StudentRepository

from schema.request import CreateStudentRequest, LogInRequest, UpdatePasswordRequest
from schema.response import JWTResponse, StudentSchema

from functions.student import StudentFunction

import bcrypt

router = APIRouter(prefix="/students")


@router.get("/", status_code=200, tags=["Students"])
def get_students_handler(repo: StudentRepository = Depends()):
    return repo.get_all_entities()


@router.get("/{id}", status_code=200, tags=["Students"])
def get_student_by_id_handler(
    id: str,
    repo: StudentRepository = Depends()
):
    student = repo.get_entity_by_id(id=id)

    if student:
        return student
    raise HTTPException(
        status_code=404, detail=f"Not found student infomation of id = {id}")


@router.post("/", status_code=201, tags=["Students"])
def post_create_id_handler(
    request: CreateStudentRequest,
    repo: StudentRepository = Depends()
) -> StudentSchema:
    student: Students = Students.create(request=request)
    student: Students = repo.create_entity(student=student)
    return StudentSchema.from_orm(student)


@router.patch("/{id}", status_code=200, tags=["Students"])
def patch_update_student_pw_by_id_handler(
    id: str,
    request: UpdatePasswordRequest,
    repo: StudentRepository = Depends(),
    student_func: StudentFunction = Depends()
):
    student = repo.get_entity_by_id(id=id)

    if student:
        encrypted_pw = student_func.encrypt_pw(request.pw)
        repo.update_entity_by_id(id=id, pw=encrypted_pw)
    else:
        raise HTTPException(status_code=404, detail="Student Not Found")


@router.delete("/{id}", status_code=204, tags=["Students"])
def delete_student_handler(
    id: str,
    repo: StudentRepository = Depends()
):
    student = repo.get_entity_by_id(id=id)

    if student:
        repo.delete_entity_by_id(id=id)
    else:
        raise HTTPException(status_code=404, detail="Student Not Found")


@router.post("/log-in", tags=["Students"])
def post_student_login_handler(
    request: LogInRequest,
    repo: StudentRepository = Depends(),
    student_func: StudentFunction = Depends()
):
    student = repo.get_entity_by_id(id=request.id)

    if not student:
        raise HTTPException(status_code=404, detail="Student Not Found")

    verified: bool = student_func.verify_pw(request.pw, student.pw)

    if not verified:
        raise HTTPException(status_code=401, detail="Password is incorrect.")

    access_token = student_func.create_jwt(student.id)
    return JWTResponse(access_token=access_token)
