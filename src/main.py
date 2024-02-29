# from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_database
from database_orm import Students

# from fastapi.middleware.cors import CORSMiddleware

# import config
# from apis.common import common_router
# from apis.posts import post_router
# from database import close_db, create_db_and_tables


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     await create_db_and_tables()
#     yield
#     await close_db()

# app = FastAPI(lifespan=lifespan)

# app.include_router(common_router)
# app.include_router(post_router)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=config.cors.origins.split(","),
#     allow_credentials=True,
#     allow_methods=config.cors.methods.split(","),
#     allow_headers=config.cors.headers.split(","),
# )

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
    query_result = session.scalar(select(Students).where(Students.student_id == student_id))
    if not query_result:
        raise HTTPException(status_code=404, detail=f"Not found student infomation of id = {student_id}")
    return query_result