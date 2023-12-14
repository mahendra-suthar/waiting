from datetime import time
from fastapi import Request, Form
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, Response, RedirectResponse
from typing import Optional
from fastapi.encoders import jsonable_encoder

from .helpers import jinja_variables_for_employee_service
from ..forms import EmployeeServiceForm
from .schema import RegisterEmployeeService
from ..queries import insert_item, get_item, update_item, delete_item
from ..utils import prepare_dropdown_for_forms

router = APIRouter()
templates = Jinja2Templates(directory=r"templates")
employee_service_collection = 'employee_service'
service_collection = 'service'
employee_collection = 'employee'


@router.get("/employee_service", response_class=HTMLResponse)
async def employee_service(request: Request) -> HTMLResponse:
    columns, data, name, table_name = jinja_variables_for_employee_service()
    modify = True
    return templates.TemplateResponse("admin/index.html", context=locals())


@router.get("/employee_service/new", response_class=HTMLResponse)
def show_add_employee_service_form(request: Request) -> HTMLResponse:
    form = EmployeeServiceForm(request)
    form.service_id.choices = prepare_dropdown_for_forms(collection_name=service_collection, label='name', value='_id')
    form.employee_id.choices = prepare_dropdown_for_forms(
        collection_name=employee_collection, label='email', value='_id'
    )
    name = "Employee Service"
    return templates.TemplateResponse("admin/create.html", context=locals())


@router.post("/employee_service/new", response_class=HTMLResponse)
async def save_employee_service_form(
    request: Request,
    service_id: str = Form(...),
    employee_id: str = Form(...),
    description: str = Form(...),
    service_fee: float = Form(...),
    # fee_type: int = Form(...),
    start_time: time = Form(...),
    end_time: time = Form(...),
    duration: int = Form(...),
) -> Response:
    form = EmployeeServiceForm(request=request)
    form.service_id.choices = prepare_dropdown_for_forms(collection_name=service_collection, label='name', value='_id')
    form.employee_id.choices = prepare_dropdown_for_forms(
        collection_name=employee_collection, label='email', value='_id'
    )
    form.service_id.data = service_id
    form.employee_id.data = employee_id
    form.description.data = description
    form.service_fee.data = service_fee
    # form.fee_type.data = fee_type
    form.start_time.data = start_time
    form.end_time.data = end_time
    form.duration.data = duration

    if await form.validate():
        item_data = RegisterEmployeeService(
            service_id=service_id,
            employee_id=employee_id,
            description=description,
            service_fee=service_fee,
            fee_type=2,
            start_time=start_time,
            end_time=end_time,
            duration=duration,
        )
        data_dict = jsonable_encoder(item_data)
        insert_item(employee_service_collection, data_dict)
        return RedirectResponse(
            "/web/employee_service", status_code=302
        )

    return templates.TemplateResponse("admin/create.html", context=locals())