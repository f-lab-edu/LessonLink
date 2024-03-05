from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database.database import get_database
from database.database_orm import Students
from schema.request import CreateStudentRequest

router = APIRouter(prefix="/students")

@router.get("/", status_code=200)
def get_students_handler(session: Session = Depends(get_database)):
    return list(session.scalars(select(Students)))


@router.get("/{student_id}", status_code=200)
def get_students_by_id_handler(
    student_id: str,
    session: Session = Depends(get_database)
):
    query_result = session.scalar(select(Students).where(Students.student_id == student_id))
    if query_result:
        return query_result
    raise HTTPException(status_code=404, detail=f"Not found student infomation of id = {student_id}")

@router.post("/", status_code=201)
def post_create_student_id_handler(
    request: CreateStudentRequest,
    session: Session = Depends(get_database)
):
    student = Students(
        student_id=request.student_id,
        student_pw=request.student_pw,
        student_name=request.student_name,
        student_contact=request.student_contact,
        student_email=request.student_email,
        student_birth_date=request.student_birth_date,
        student_gender=request.student_gender,
        join_date=date.today()
    )

    query_result = session.scalar(select(Students).where(Students.student_id == student.student_id))
    
    if not query_result:
        session.add(student)
        session.commit()
    else:
        raise HTTPException(status_code=409, detail="이미 존재하는 ID입니다.")
    
@router.patch("/{student_id}", status_code=200)
def patch_update_student_pw_by_id_handler(
    student_id: str,
    student_pw: str,
    session: Session = Depends(get_database)
):
    query_result = session.scalar(select(Students).where(Students.student_id == student_id))

    if query_result:
        student = session.execute(select(Students).filter_by(student_id=student_id)).scalar_one()
        student.student_pw = student_pw
        session.commit()
    else:
        raise HTTPException(status_code=404, detail="Student Not Found")
    
@router.delete("/{student_id}", status_code=204)
def delete_student_handler(
    student_id: str,
    session: Session = Depends(get_database)
):
    query_result = session.scalar(select(Students).where(Students.student_id == student_id))

    if query_result:
        session.execute(delete(Students).where(Students.student_id == student_id))
        session.commit()
    else:
        raise HTTPException(status_code=404, detail="Student Not Found")