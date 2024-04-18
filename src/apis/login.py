import os

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
template_dir = os.path.join(base_dir, 'templates')
templates = Jinja2Templates(directory=template_dir)

router = APIRouter(prefix="/log-in")


@router.get("/students", tags=["Login"], response_class=HTMLResponse)
def get_student_login_handler(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
