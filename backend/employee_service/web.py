from fastapi import Request, Form
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, Response, RedirectResponse
from typing import Optional
from fastapi.encoders import jsonable_encoder

from .helpers import jinja_variables_for_employee_service
from ..forms import EmployeeServiceForm
# from .schema import RegisterEmployee, UpdateEmployee
from ..queries import insert_item, get_item, update_item, delete_item

router = APIRouter()
templates = Jinja2Templates(directory=r"templates")
employee_service_collection = 'employee_service'


@router.get("/employee_service", response_class=HTMLResponse)
async def employee_service(request: Request) -> HTMLResponse:
    columns, data, name, table_name = jinja_variables_for_employee_service()
    modify = True
    return templates.TemplateResponse("admin/index.html", context=locals())


@router.get("/employee_service/new", response_class=HTMLResponse)
def show_add_employee_service_form(request: Request) -> HTMLResponse:
    form = EmployeeServiceForm(request)
    name = "Employee Service"
    return templates.TemplateResponse("admin/create.html", context=locals())