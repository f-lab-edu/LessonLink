
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_database
from database_orm import Students


app = FastAPI()

@app.get("/")
def root_handler():
    return {"Hello":"World!"}

@app.get("/students", status_code=200)
def get_students_handler(session: Session = Depends(get_database)):
    return list(session.scalars(select(Students)))

@app.get("/students/{student_id}", status_code=200)
def get_students_by_id_handler(
        student_id: str,
        session: Session = Depends(get_database)
        ):
    query_result = session.scalar(
        select(Students).where(Students.student_id == student_id)
        )
    
    if not query_result:
        error_msg = f"Not found student infomation of id = {student_id}"
        raise HTTPException(status_code=404, 
                            detail=error_msg)
    return query_result