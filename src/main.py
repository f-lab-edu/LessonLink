from fastapi import FastAPI
from apis import students, instructors, courses

app = FastAPI()
app.include_router(students.router)
app.include_router(instructors.router)

@app.get("/")
def root_handler():
    return {"Hello":"World!"}