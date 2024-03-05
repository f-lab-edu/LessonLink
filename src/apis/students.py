from sqlalchemy import select
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database.database import get_database
from database.database_orm import Students
from schema.request import StudentRequest


router = APIRouter(prefix="/students")

@router.get("/", status_code=200)
def get_students_handler(session: Session = Depends(get_database)):
    return list(session.scalars(select(Students)))

@router.get("/{student_id}", status_code=200)
def get_students_by_id_handler(
        student_id: str,
        session: Session = Depends(get_database)
        ):
    query_result = session.scalar(
        select(Students).where(Students.student_id == student_id)
        )

    if not query_result:
        error_msg = f"Not found student infomation of id = {student_id}"

        raise HTTPException(
            status_code=404,
            detail=error_msg
            )

    return query_result


@router.post("/", status_code=201)
def post_students_handler(
    post_student: StudentRequest,
    session: Session = Depends(get_database)
    ):

    student = Students(
        student_id=post_student.student_id,
        student_pw=post_student.student_pw,
        student_name=post_student.student_name,
        student_contact=post_student.student_contact,
        student_email=post_student.student_email,
        student_birth_date=post_student.student_birth_date,
        student_gender=post_student.student_gender,
        join_date=post_student.join_date,
        )

    try:
        session.add(student)
        session.commit()
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(status_code=409, detail="ID is already existed.")