


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from database.database import get_database
from database.database_orm import Students

router = APIRouter(prefix="/students")

@router.get("/students", status_code=200)
def get_students_handler(session: Session = Depends(get_database)):
    return list(session.scalars(select(Students)))


@router.get("/students/{student_id}", status_code=200)
def get_students_by_id_handler(
        student_id: str,
        session: Session = Depends(get_database)
        ):
    query_result = session.scalar(select(Students).where(Students.student_id == student_id))
    if not query_result:
        raise HTTPException(status_code=404, detail=f"Not found student infomation of id = {student_id}")
    return query_result