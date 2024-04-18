from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os


router = APIRouter(prefix="/payments")

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
template_dir = os.path.join(base_dir, 'templates')
templates = Jinja2Templates(directory=template_dir)


@router.get("/", status_code=200, tags=["Payments"], response_class=HTMLResponse)
def get_payments_handler(request: Request):
    return templates.TemplateResponse("payment_form.html", {"request": request})
