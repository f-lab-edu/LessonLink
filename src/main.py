from fastapi import FastAPI, APIRouter
from apis import students

app = FastAPI()
router = app.include_router(students.router)

@app.get("/")
def root_handler():
    return {"Hello":"World!"}