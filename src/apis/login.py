import os

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from database.StudentRepository import StudentRepository
from database.database_orm import Instructors, Students
from functions.student import StudentFunction
from schema.request import LogInRequest
from database.InstructorRepository import InstructorRepository
from functions.instructor import InstructorFunction
from schema.response import JWTResponse

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
template_dir = os.path.join(base_dir, 'templates')
templates = Jinja2Templates(directory=template_dir)

router = APIRouter(prefix="/log-in")


@router.get("/students", tags=["Login"], response_class=HTMLResponse)
def get_student_login_handler(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/students", tags=["Login"])
def post_student_login_handler(
    request: LogInRequest,
    repo: StudentRepository = Depends(),
    student_func: StudentFunction = Depends()
):

    student: Students | None = repo.get_entity_by_id(id=request.id)

    if not student:
        raise HTTPException(status_code=404, detail="Student Not Found")

    verified: bool = student_func.verify_pw(request.pw, student.pw)

    if not verified:
        raise HTTPException(status_code=401, detail="Password is incorrect.")

    access_token: str = student_func.create_jwt(student.id)
    return JWTResponse(access_token=access_token)


@router.post("/instructors", tags=["Login"])
def post_instructor_login_handler(
    request: LogInRequest,
    repo: InstructorRepository = Depends(),
    instructor_func: InstructorFunction = Depends()
):
    instructor: Instructors | None = repo.get_entity_by_id(id=request.id)

    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor Not Found")

    verified: bool = instructor_func.verify_pw(request.pw, instructor.pw)

    if not verified:
        raise HTTPException(status_code=401, detail="Password is incorrect.")

    access_token: str = instructor_func.create_jwt(instructor.id)
    return JWTResponse(access_token=access_token)