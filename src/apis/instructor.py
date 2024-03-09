from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import delete, select, update

from database.database import get_database
from database.database_orm import Instructors
from schema.request import CreateInstructorRequest

router = APIRouter(prefix="/instructors")

@router.get("/", status_code=200)
def get_instructor_handler(session: Session = Depends(get_database)):
    return list(session.scalars(select(Instructors)))

@router.get("/{instructor_id}", status_code=200)
def get_instructor_by_id_handler(
    instructor_id: str,
    session: Session = Depends(get_database)
):
    query_result = session.scalar(select(Instructors).where(Instructors.instructor_id == instructor_id))
    
    if query_result:
        return query_result
    raise HTTPException(status_code=404, detail=f"Not found student infomation of id = {instructor_id}")

@router.post("/", status_code=201)
def post_create_instructor_handler(
    request: CreateInstructorRequest,
    session: Session = Depends(get_database)
):
    instructor = Instructors(
        instructor_id=request.instructor_id,
        instructor_pw=request.instructor_pw,
        instructor_name=request.instructor_name,
        instructor_contact=request.instructor_contact,
        instructor_email=request.instructor_email,
        subject=request.subject,
    )

    query_result = session.scalar(select(Instructors).where(Instructors.instructor_id == instructor.instructor_id))
    
    if not query_result:
        session.add(instructor)
        session.commit()
    else:
        raise HTTPException(status_code=409, detail="이미 존재하는 ID입니다.")
    
@router.patch("/{instructor_id}", status_code=200)
def patch_update_instructor_pw_by_id_handler(
    instructor_id: str,
    instructor_pw: str,
    session: Session = Depends(get_database)
):
    query_result = session.scalar(select(Instructors).where(Instructors.instructor_id == instructor_id))

    if query_result:
        instructor = session.execute(select(Instructors).filter_by(instructor_id=instructor_id)).scalar_one()
        instructor.instructor_pw = instructor_pw
        session.commit()
    else:
        raise HTTPException(status_code=404, detail="Instructor Not Found")
    
@router.delete("/{instructor_id}", status_code=204)
def delete_student_handler(
    instructor_id: str,
    session: Session = Depends(get_database)
):
    query_result = session.scalar(select(Instructors).where(Instructors.instructor_id == instructor_id))

    if query_result:
        session.execute(delete(Instructors).where(Instructors.instructor_id == instructor_id))
        session.commit()
    else:
        raise HTTPException(status_code=404, detail="Instructor Not Found")