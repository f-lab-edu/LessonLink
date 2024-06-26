from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from apis import (
    students, instructors, courses,
    classrooms, schedules, reservations,
    payments, login, bucket
)

app = FastAPI()
app.include_router(students.router)
app.include_router(instructors.router)
app.include_router(courses.router)
app.include_router(classrooms.router)
app.include_router(schedules.router)
app.include_router(reservations.router)
app.include_router(payments.router)
app.include_router(login.router)
app.include_router(bucket.router)

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def root_handler(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
