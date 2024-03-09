from fastapi import FastAPI
from apis import students, instructor

app = FastAPI()
app.include_router(students.router)
app.include_router(instructor.router)

@app.get("/")
def root_handler():
    return {"Hello":"World!"}