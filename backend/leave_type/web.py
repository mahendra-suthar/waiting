from fastapi import Request, Form, HTTPException
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, Response, RedirectResponse
from fastapi.encoders import jsonable_encoder

from ..forms import LeaveTypeForm, LeaveBalanceForm
from ..constants import LEAVE_PENDING
from .helpers import jinja_variables_for_leave_type, jinja_variables_for_leave_balance
from .schema import RegisterLeaveBalance, RegisterLeaveType
from ..queries import insert_item, filter_data
from ..utils import prepare_dropdown_for_forms, get_current_timestamp_utc


router = APIRouter()
templates = Jinja2Templates(directory=r"templates")
leave_type_collection = 'leave_type'
business_collection = 'business'
employee_collection = 'employee'
leave_collection = 'leave'
leave_balance_collection = 'leave_balance'


# Leave Type
@router.get("/leave_type", response_class=HTMLResponse)
async def get_all_leave_type(request: Request) -> HTMLResponse:
    columns, data, name, table_name = jinja_variables_for_leave_type()
    modify = True
    return templates.TemplateResponse("admin/index.html", context=locals())


@router.get("/leave_type/new", response_class=HTMLResponse)
def show_add_leave_type_form(request: Request) -> HTMLResponse:
    form = LeaveTypeForm(request)
    form.business_id.choices = prepare_dropdown_for_forms(collection_name=business_collection, label='email',
                                                          value='_id')
    name = "Leave Type"
    return templates.TemplateResponse("admin/create.html", context=locals())


@router.post("/leave_type/new", response_class=HTMLResponse)
async def save_leave_type_form(
    request: Request,
    business_id: str = Form(...),
    name: str = Form(...),
    description: str = Form(...)
) -> Response:
    form = LeaveTypeForm(request=request)
    form.business_id.choices = prepare_dropdown_for_forms(collection_name=business_collection, label='email',
                                                          value='_id')
    form.business_id.data = business_id
    form.name.data = name
    form.description.data = description
    if await form.validate():
        item_data = RegisterLeaveType(
            business_id=business_id,
            name=name,
            description=description
        )
        print("item_data", item_data)
        data_dict = jsonable_encoder(item_data)
        inserted_id = insert_item(leave_type_collection, data_dict)
        return RedirectResponse(
            "/web/leave_type", status_code=302
        )
    else:
        # Handle validation errors
        print("Validation errors:", form.errors)

    return templates.TemplateResponse("admin/create.html", context=locals())


# Leave Balance
@router.get("/leave_balance", response_class=HTMLResponse)
async def get_all_leave_balance(request: Request) -> HTMLResponse:
    columns, data, name, table_name = jinja_variables_for_leave_balance()
    modify = True
    return templates.TemplateResponse("admin/index.html", context=locals())


@router.get("/leave_balance/new", response_class=HTMLResponse)
def show_add_leave_balance_form(request: Request) -> HTMLResponse:
    form = LeaveBalanceForm(request)
    form.employee_id.choices = prepare_dropdown_for_forms(collection_name=employee_collection, label='email',
                                                          value='_id')
    form.leave_type_id.choices = prepare_dropdown_for_forms(collection_name=leave_type_collection, label='name',
                                                            value='_id')
    name = "Leave Balance"
    return templates.TemplateResponse("admin/create.html", context=locals())


@router.post("/leave_balance/new", response_class=HTMLResponse)
async def save_leave_balance_form(
    request: Request,
    employee_id: str = Form(...),
    leave_type_id: str = Form(...),
    leave_year: int = Form(...),
    entitlement: int = Form(...),
    consumed: int = Form(...),
    available: int = Form(...)
) -> Response:
    form = LeaveBalanceForm(request=request)
    form.employee_id.choices = prepare_dropdown_for_forms(collection_name=employee_collection, label='email',
                                                          value='_id')
    form.leave_type_id.choices = prepare_dropdown_for_forms(collection_name=leave_type_collection, label='name',
                                                            value='_id')
    form.employee_id.data = employee_id
    form.leave_type_id.data = leave_type_id
    form.leave_year.data = leave_year
    form.entitlement.data = entitlement
    form.consumed.data = consumed
    form.available.data = available
    if await form.validate():
        item_data = RegisterLeaveBalance(
            employee_id=employee_id,
            leave_type_id=leave_type_id,
            leave_year=leave_year,
            entitlement=entitlement,
            consumed=consumed,
            available=available
        )
        print("item_data", item_data)
        data_dict = jsonable_encoder(item_data)
        inserted_id = insert_item(leave_balance_collection, data_dict)
        return RedirectResponse(
            "/web/leave_balance", status_code=302
        )
    else:
        # Handle validation errors
        print("Validation errors:", form.errors)

    return templates.TemplateResponse("admin/create.html", context=locals())