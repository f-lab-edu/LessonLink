from fastapi import APIRouter, Depends, HTTPException

from database.database_repo import CoursesRepository
from schema.request import CreateCourseRequest, UpdateCourseRequest
from schema.response import CourseSchema
from database.database_orm import Courses

router = APIRouter(prefix="/courses")


@router.get("/", status_code=200, tags=["Courses"])
def get_courses_handler(repo: CoursesRepository = Depends()):
    return repo.get_all_entities()


@router.get("/{id}", status_code=200, tags=["Courses"])
def get_course_by_id_handler(
    id: int,
    repo: CoursesRepository = Depends()
):
    course = repo.get_entity_by_id(id=id)

    if course:
        return course
    raise HTTPException(
        status_code=404, detail=f"Not found course infomation of id = {id}")


@router.post("/", status_code=201, tags=["Courses"])
def post_create_course_handler(
    request: CreateCourseRequest,
    repo: CoursesRepository = Depends()
) -> CourseSchema:
    course: Courses = Courses.create(request=request)
    course: Courses = repo.create_entity(course=course)
    return CourseSchema.from_orm(course)


@router.patch("/{id}", status_code=200, tags=["Courses"])
def patch_course_handler(
    id: int,
    request: UpdateCourseRequest,
    repo: CoursesRepository = Depends()
):
    course = repo.get_entity_by_id(id=id)

    if course:
        repo.update_entity_by_id(id=id, request=request)
    else:
        raise HTTPException(status_code=404, detail="Course Not Found")


@router.delete("/{id}", status_code=204, tags=["Courses"])
def delete_student_handler(
    id: int,
    repo: CoursesRepository = Depends()
):
    course = repo.get_entity_by_id(id=id)

    if course:
        repo.delete_entity_by_id(id=id)
    else:
        raise HTTPException(status_code=404, detail="Course Not Found")
