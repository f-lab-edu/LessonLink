from fastapi import APIRouter, Depends, HTTPException

from database.database_orm import Students
from database.database_repo import StudentRepository

from schema.request import CreateStudentRequest, UpdatePasswordRequest
from schema.response import StudentSchema

from functions.student import StudentFunction
from functions.security import get_access_token

router = APIRouter(prefix="/students")


@router.get("/", status_code=200, tags=["Students"])
def get_students_handler(
    access_token: str = Depends(get_access_token),
    student_func: StudentFunction = Depends(),
    repo: StudentRepository = Depends()
):

    payload: dict = student_func.decode_jwt(access_token=access_token)
    role: str = payload['role']
    if not (role == 'admin'):
        raise HTTPException(
            status_code=401, detail=f"Admin only allowed.")

    return repo.get_all_entities()


@router.get("/{id}", status_code=200, tags=["Students"])
def get_student_by_id_handler(
    id: str,
    access_token: str = Depends(get_access_token),
    student_func: StudentFunction = Depends(),
    repo: StudentRepository = Depends()
):

    payload: dict = student_func.decode_jwt(access_token=access_token)
    role: str = payload['role']
    sub: str = payload['sub']
    if not (role == 'admin' or sub == id):
        raise HTTPException(
            status_code=401, detail=f"Not allowed.")

    student: Students | None = repo.get_entity_by_id(id=id)

    if student:
        return student
    raise HTTPException(
        status_code=404, detail=f"Not found student infomation of id = {id}")


@router.post("/", status_code=201, tags=["Students"])
def post_create_student_handler(
    request: CreateStudentRequest,
    repo: StudentRepository = Depends()
) -> StudentSchema:

    student: Students = Students.create(request=request)
    student: Students = repo.create_entity(student=student)
    return StudentSchema.model_validate(student)


@router.patch("/{id}", status_code=200, tags=["Students"])
def patch_update_student_pw_by_id_handler(
    id: str,
    request: UpdatePasswordRequest,
    repo: StudentRepository = Depends(),
    access_token: str = Depends(get_access_token),
    student_func: StudentFunction = Depends()
):

    payload: dict = student_func.decode_jwt(access_token=access_token)
    role: str = payload['role']
    sub: str = payload['sub']
    if not (role == 'admin' or sub == id):
        raise HTTPException(
            status_code=401, detail=f"Not allowed.")

    student: Students | None = repo.get_entity_by_id(id=id)

    if student:
        encrypted_pw = student_func.encrypt_pw(request.pw)
        repo.update_entity_by_id(id=id, pw=encrypted_pw)
    else:
        raise HTTPException(status_code=404, detail="Student Not Found")


@router.delete("/{id}", status_code=204, tags=["Students"])
def delete_student_handler(
    id: str,
    access_token: str = Depends(get_access_token),
    student_func: StudentFunction = Depends(),
    repo: StudentRepository = Depends()
):

    payload: dict = student_func.decode_jwt(access_token=access_token)
    role: str = payload['role']
    sub: str = payload['sub']
    if not (role == 'admin' or sub == id):
        raise HTTPException(
            status_code=401, detail=f"Not allowed.")

    student: Students | None = repo.get_entity_by_id(id=id)

    if student:
        repo.delete_entity_by_id(id=id)
    else:
        raise HTTPException(status_code=404, detail="Student Not Found")


