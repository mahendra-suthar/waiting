from fastapi import Request, Form
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, Response, RedirectResponse
from typing import Optional
from fastapi.encoders import jsonable_encoder

from .helpers import jinja_variables_for_employees
from ..forms import EmployeeForm
from .schema import RegisterEmployee, UpdateEmployee
from ..queries import insert_item, get_item, update_item, delete_item

router = APIRouter()
templates = Jinja2Templates(directory=r"templates")
employee_collection = 'employee'


@router.get("/employee", response_class=HTMLResponse)
async def users(request: Request) -> HTMLResponse:
    columns, data, name, table_name = jinja_variables_for_employees()
    modify = True
    return templates.TemplateResponse("admin/index.html", context=locals())


@router.get("/employee/new", response_class=HTMLResponse)
def show_add_employee_form(request: Request) -> HTMLResponse:
    form = EmployeeForm(request)
    name = "Employee"
    return templates.TemplateResponse("admin/create.html", context=locals())


@router.post("/employee/new", response_class=HTMLResponse)
async def save_business_form(
    request: Request,
    merchant_id: str = Form(...),
    email: str = Form(...),
    # password: str = Form(...),
    country_code: str = Form(...),
    phone_number: str = Form(...),
    user_id: str = Form(...),
    joined_date: Optional[int] = Form(None),
    department_id: Optional[str] = Form(None),
    employee_number: Optional[int] = Form(None)
) -> Response:
    form = EmployeeForm(request=request)
    form.merchant_id.data = merchant_id
    form.email.data = email
    form.user_id = user_id
    form.country_code.data = country_code
    form.phone_number.data = phone_number
    form.joined_date.data = joined_date
    form.department_id.data = department_id
    form.employee_number.data = employee_number

    if await form.validate():
        item_data = RegisterEmployee(
            merchant_id=merchant_id,
            email=email,
            # password=password,
            country_code=country_code,
            phone_number=phone_number,
            joined_date=joined_date,
            department_id=department_id,
            employee_number=employee_number,
            user_id=user_id
        )
        data_dict = jsonable_encoder(item_data)
        insert_item(employee_collection, data_dict)
        return RedirectResponse(
            "/web/employee", status_code=302
        )

    return templates.TemplateResponse("admin/create.html", context=locals())


@router.get("/employee/update/{item_id}", response_class=HTMLResponse)
def show_employee_update_form(request: Request, item_id: str) -> HTMLResponse:
    obj = get_item(employee_collection, item_id=item_id)
    obj = obj['data']
    dict_data = {
        "merchant_id": obj['merchant_id'],
        "email": obj['email'],
        "country_code": obj['country_code'],
        "phone_number": obj['phone_number'],
        "joined_date": obj['joined_date'],
        "department_id": obj['department_id'],
        "employee_number": obj['employee_number']
    }
    form = EmployeeForm(request=request, data=dict_data)
    name = "Employee"
    return templates.TemplateResponse("admin/update.html", context=locals())


@router.post("/employee/update/{item_id}", response_class=HTMLResponse)
async def save_employee_update_form(
    request: Request,
    item_id: str,
    merchant_id: str = Form(...),
    email: str = Form(...),
    country_code: str = Form(...),
    phone_number: str = Form(...),
    joined_date: Optional[int] = Form(None),
    department_id: Optional[str] = Form(None),
    employee_number: Optional[int] = Form(None)
) -> RedirectResponse:
    name = 'Employee'

    form = EmployeeForm(request=request)
    form.employee_id.data = item_id
    form.merchant_id.data = merchant_id
    form.email.data = email
    form.country_code.data = country_code
    form.phone_number.data = phone_number
    form.joined_date.data = joined_date
    form.department_id.data = department_id
    form.employee_number.data = employee_number

    if await form.validate():
        item_data = UpdateEmployee(
            merchant_id=merchant_id,
            email=email,
            country_code=country_code,
            phone_number=phone_number,
            joined_date=joined_date,
            department_id=department_id,
            employee_number=employee_number,
        )

        data_dict = jsonable_encoder(item_data)
        update_item(employee_collection, item_id, data_dict)
        return RedirectResponse(
            "/web/employee", status_code=302
        )

    return templates.TemplateResponse("admin/update.html", context=locals())


@router.get("/employee/delete/{item_id}", response_class=HTMLResponse)
def save_employee_update_form(item_id: str) -> RedirectResponse:
    delete_item(employee_collection, item_id)
    return RedirectResponse(
        "/web/employee", status_code=302
    )