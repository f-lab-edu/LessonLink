import bcrypt
from fastapi import APIRouter, Depends, HTTPException

from database.database_orm import Instructors
from schema.request import CreateInstructorRequest, LogInRequest, UpdatePasswordRequest
from database.InstructorRepository import InstructorRepository
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

    payload: dict = instructor_func.decode_jwt(access_token=access_token)
    role: str = payload['role']
    if not (role == 'admin'):
        raise HTTPException(
            status_code=401, detail=f"Only admin can look up all instructor infomation.")

    return repo.get_all_entities()


@router.get("/{id}", status_code=200, tags=["Instructors"])
def get_instructor_by_id_handler(
    id: str,
    access_token: str = Depends(get_access_token),
    instructor_func: InstructorFunction = Depends(),
    repo: InstructorRepository = Depends()
):

    payload: dict = instructor_func.decode_jwt(access_token=access_token)
    role: str = payload['role']
    sub: str = payload['sub']
    if not (role == 'admin' or sub == id):
        raise HTTPException(
            status_code=401, detail=f"Not allowed.")

    instructor: Instructors | None = repo.get_entity_by_id(id=id)

    if instructor:
        return instructor
    else:
        raise HTTPException(
            status_code=404, detail=f"Not found instructor infomation of id = {id}")


@router.post("/", status_code=201, tags=["Instructors"])
def post_create_instructor_handler(
    request: CreateInstructorRequest,
    repo: InstructorRepository = Depends()
):

    instructor: Instructors = Instructors.create(request=request)
    instructor: Instructors = repo.create_entity(instructor=instructor)
    return InstructorSchema.model_validate(instructor)


@router.patch("/{id}", status_code=200, tags=["Instructors"])
def patch_update_instructor_pw_by_id_handler(
    id: str,
    request: UpdatePasswordRequest,
    access_token: str = Depends(get_access_token),
    instructor_func: InstructorFunction = Depends(),
    repo: InstructorRepository = Depends()
):

    payload: dict = instructor_func.decode_jwt(access_token=access_token)
    role: str = payload['role']
    sub: str = payload['sub']
    if not (role == 'admin' or sub == id):
        raise HTTPException(
            status_code=401, detail=f"Not allowed.")

    instructor: Instructors | None = repo.get_entity_by_id(id=id)

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
    payload: dict = instructor_func.decode_jwt(access_token=access_token)
    role: str = payload['role']
    sub: str = payload['sub']
    if not (role == 'admin' or sub == id):
        raise HTTPException(
            status_code=401, detail=f"Not allowed.")

    instructor: Instructors | None = repo.get_entity_by_id(id=id)

    if instructor:
        repo.delete_entity_by_id(id=id)
    else:
        raise HTTPException(status_code=404, detail="Instructor Not Found")



