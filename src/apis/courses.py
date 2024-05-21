from fastapi import APIRouter, Depends, HTTPException

from database.database_repo import CoursesRepository
from schema.request import CreateCourseRequest, UpdateCourseRequest
from schema.response import CourseSchema
from database.database_orm import Courses
from functions.security import get_access_token
from functions.instructor import InstructorFunction

router = APIRouter(prefix="/courses")


@router.get("/", status_code=200, tags=["Courses"])
def get_courses_handler(
    _: str = Depends(get_access_token),
    repo: CoursesRepository = Depends()
):
    return repo.get_all_entities()


@router.get("/{id}", status_code=200, tags=["Courses"])
def get_course_by_id_handler(
    id: int,
    _: str = Depends(get_access_token),
    repo: CoursesRepository = Depends()
):
    course: Courses | None = repo.get_entity_by_id(id=id)

    if course:
        return course
    raise HTTPException(
        status_code=404, detail=f"Not found course infomation of id = {id}")


@router.post("/", status_code=201, tags=["Courses"])
def post_create_course_handler(
    request: CreateCourseRequest,
    access_token: str = Depends(get_access_token),
    instructor_func: InstructorFunction = Depends(),
    repo: CoursesRepository = Depends()
) -> CourseSchema:

    payload: dict = instructor_func.decode_jwt(access_token=access_token)
    role: str = payload['role']

    if role == 'student':
        raise HTTPException(
            status_code=401, detail=f"Student can't add course.")

    course: Courses = Courses.create(request=request)
    course: Courses = repo.create_entity(course=course)
    return CourseSchema.model_validate(course)


@router.patch("/{id}", status_code=200, tags=["Courses"])
def patch_course_handler(
    id: int,
    request: UpdateCourseRequest,
    access_token: str = Depends(get_access_token),
    instructor_func: InstructorFunction = Depends(),
    repo: CoursesRepository = Depends()
):
    payload: dict = instructor_func.decode_jwt(access_token=access_token)
    role: str = payload['role']

    if role == 'student':
        raise HTTPException(
            status_code=401, detail=f"Student can't edit course.")

    course: Courses | None = repo.get_entity_by_id(id=id)

    if course:
        repo.update_entity_by_id(id=id, request=request)
    else:
        raise HTTPException(status_code=404, detail="Course Not Found")


@router.delete("/{id}", status_code=204, tags=["Courses"])
def delete_course_handler(
    id: int,
    access_token: str = Depends(get_access_token),
    instructor_func: InstructorFunction = Depends(),
    repo: CoursesRepository = Depends()
):
    payload: dict = instructor_func.decode_jwt(access_token=access_token)
    role: str = payload['role']

    if role == 'student':
        raise HTTPException(
            status_code=401, detail=f"Student can't delete course.")

    course: Courses | None = repo.get_entity_by_id(id=id)

    if course:
        repo.delete_entity_by_id(id=id)
    else:
        raise HTTPException(status_code=404, detail="Course Not Found")
