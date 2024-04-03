import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from database.database_orm import Instructors
from schema.request import CreateInstructorRequest, LogInRequest, UpdatePasswordRequest
from database.database_repo import InstructorRepository
from schema.response import InstructorSchema, JWTResponse
from functions.instructor import InstructorFunction
from functions.security import get_access_token

router = APIRouter(prefix="/instructors")


@router.get("/", status_code=200, tags=["Instructors"])
def get_instructor_handler(
    access_token: str = Depends(get_access_token),
    instructor_func: InstructorFunction = Depends(),
    repo: InstructorRepository = Depends()
):
    payload = instructor_func.decode_jwt(access_token=access_token)
    role = payload['role']
    if not (role == 'admin'):
        raise HTTPException(
            status_code=401, detail=f"Admin only allowed.")

    return repo.get_all_entities()


@router.get("/{id}", status_code=200, tags=["Instructors"])
def get_instructor_by_id_handler(
    id: str,
    access_token: str = Depends(get_access_token),
    instructor_func: InstructorFunction = Depends(),
    repo: InstructorRepository = Depends()
):
    payload = instructor_func.decode_jwt(access_token=access_token)
    role = payload['role']
    sub = payload['sub']
    if not (role == 'admin' or sub == id):
        raise HTTPException(
            status_code=401, detail=f"Not allowed.")

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
    access_token: str = Depends(get_access_token),
    instructor_func: InstructorFunction = Depends(),
    repo: InstructorRepository = Depends()
):
    payload = instructor_func.decode_jwt(access_token=access_token)
    role = payload['role']
    sub = payload['sub']
    if not (role == 'admin' or sub == id):
        raise HTTPException(
            status_code=401, detail=f"Not allowed.")

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
    access_token: str = Depends(get_access_token),
    instructor_func: InstructorFunction = Depends(),
    repo: InstructorRepository = Depends()
):
    payload = instructor_func.decode_jwt(access_token=access_token)
    role = payload['role']
    sub = payload['sub']
    if not (role == 'admin' or sub == id):
        raise HTTPException(
            status_code=401, detail=f"Not allowed.")

    instructor = repo.get_entity_by_id(id=id)

    if instructor:
        repo.delete_entity_by_id(id=id)
    else:
        raise HTTPException(status_code=404, detail="Instructor Not Found")


@router.post("/log-in", tags=["Instructors"])
def post_student_login_handler(
    request: LogInRequest,
    repo: InstructorRepository = Depends(),
    instructor_func: InstructorFunction = Depends()
):
    instructor = repo.get_entity_by_id(id=request.id)

    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor Not Found")

    verified: bool = instructor_func.verify_pw(request.pw, instructor.pw)

    if not verified:
        raise HTTPException(status_code=401, detail="Password is incorrect.")

    access_token = instructor_func.create_jwt(instructor.id)
    return JWTResponse(access_token=access_token)
