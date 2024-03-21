from fastapi import FastAPI
from apis import students, instructors, courses, classrooms, schedules, reservations


app = FastAPI()
app.include_router(students.router)
app.include_router(instructors.router)
app.include_router(courses.router)
app.include_router(classrooms.router)
app.include_router(schedules.router)
app.include_router(reservations.router)

@app.get("/")
def root_handler():
    return {"Hello":"World!"}