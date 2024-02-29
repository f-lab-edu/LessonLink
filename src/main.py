# from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from sqlalchemy import select
from sqlalchemy.orm import Session
from database_orm import Students

import database



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
def root_handler(session: Session = Depends(database.get_db)):
    stmt = select(Students).where(Students.student_id == 'admin')
    query_result = session.scalar(stmt)
        
    return query_result



