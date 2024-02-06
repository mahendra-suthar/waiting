from fastapi import Request, Form, HTTPException
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, Response, RedirectResponse
from typing import Optional
from fastapi.encoders import jsonable_encoder

from .helpers import jinja_variables_for_leave_request
from ..forms import LeaveRequestForm, LeaveTypeForm
from ..constants import LEAVE_PENDING
from .schema import RegisterLeaveRequest, LeaveRequestActions, RegisterLeaveType
from ..queries import insert_item, filter_data
from ..utils import prepare_dropdown_for_forms, get_current_timestamp_utc
# from ..constants import QUEUE_USER_REGISTERED, QUEUE_USER_IN_PROGRESS


router = APIRouter()
templates = Jinja2Templates(directory=r"templates")
leave_collection = 'leave'
employee_collection = 'employee'
business_collection = 'business'

@router.get("/leave", response_class=HTMLResponse)
async def get_all_leave_requests(request: Request) -> HTMLResponse:
    columns, data, name, table_name = jinja_variables_for_leave_request()
    modify = True
    return templates.TemplateResponse("admin/index.html", context=locals())


@router.get("/leave/new", response_class=HTMLResponse)
def show_add_leave_request_form(request: Request) -> HTMLResponse:
    form = LeaveRequestForm(request)
    form.employee_id.choices = prepare_dropdown_for_forms(collection_name=employee_collection, label='email',
                                                          value='_id')
    name = "Leave Request"
    return templates.TemplateResponse("admin/create.html", context=locals())


@router.post("/leave/new", response_class=HTMLResponse)
async def save_leave_form(
    request: Request,
    employee_id: str = Form(...),
    start_date: int = Form(...),
    end_date: int = Form(...),
    start_duration: int = Form(...),
    end_duration: int = Form(...),
    leave_type: str = Form(...),
    note: str = Form(...),
    duration: int = Form(...),
    status: Optional[str] = Form(...),
    requested_date: Optional[int] = Form(...),
    # approval_date: Optional[int] = Form(...),
    # rejection_reason: Optional[str] = Form(...)
) -> Response:
    form = LeaveRequestForm(request=request)
    form.employee_id.choices = prepare_dropdown_for_forms(collection_name=employee_collection, label='email',
                                                          value='_id')
    form.employee_id.data = employee_id
    form.start_date.data = start_date
    form.end_date.data = end_date
    form.start_duration.data = start_date
    form.end_duration.data = end_date
    form.leave_type.data = leave_type
    form.note.data = note
    form.duration.data = duration
    form.status.data = status
    form.requested_date.data = requested_date
    # form.approval_date.data = approval_date
    # form.rejection_reason.data = rejection_reason
    if await form.validate():
        item_data = RegisterLeaveRequest(
            employee_id=employee_id,
            start_date=start_date,
            end_date=end_date,
            start_duration=start_duration,
            end_duration=end_duration,
            leave_type=leave_type,
            note=note,
            duration=duration,
            status=status,
            requested_date=get_current_timestamp_utc()
        )
        print("item_data", item_data)
        data_dict = jsonable_encoder(item_data)
        inserted_id = insert_item(leave_collection, data_dict)
        return RedirectResponse(
            "/web/leave", status_code=302
        )
    else:
        # Handle validation errors
        print("Validation errors:", form.errors)

    return templates.TemplateResponse("admin/create.html", context=locals())
