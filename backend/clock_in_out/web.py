from fastapi import Request, Form
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, Response, RedirectResponse
# from typing import Optional
from fastapi.encoders import jsonable_encoder

from .helpers import jinja_variables_for_attendance
from ..forms import AttendanceForm
from .schema import RegisterAttendance
from ..queries import insert_item, get_item, update_item, delete_item
from ..utils import prepare_dropdown_for_forms

router = APIRouter()
templates = Jinja2Templates(directory=r"templates")
attendance_collection = 'attendance'
employee_collection = 'employee'


@router.get("/attendance", response_class=HTMLResponse)
async def get_attendance_logs(request: Request) -> HTMLResponse:
    columns, data, name, table_name = jinja_variables_for_attendance()
    modify = True
    return templates.TemplateResponse("admin/index.html", context=locals())


# @router.get("/attendance/new", response_class=HTMLResponse)
# def show_add_attendance_form(request: Request) -> HTMLResponse:
#     form = AttendanceForm(request)
#     form.employee_id.choices = prepare_dropdown_for_forms(employee_collection, 'email', '_id')
#     name = "Attendance"
#     return templates.TemplateResponse("admin/create.html", context=locals())
#
#
# @router.post("/attendance/new", response_class=HTMLResponse)
# async def save_attendance_form(
#     request: Request,
#     employee_id: str = Form(...),
#     date: int = Form(...),
#     clock_in_time: int = Form(...),
#     clock_out_time: int = Form(...)
# ) -> Response:
#     form = AttendanceForm(request=request)
#     form.employee_id.choices = prepare_dropdown_for_forms(employee_collection, 'email', '_id')
#     form.employee_id.data = employee_id
#     form.date.data = date
#     form.clock_in_time.data = clock_in_time
#     form.clock_out_time.data = clock_out_time
#
#     if await form.validate():
#         item_data = RegisterAttendance(
#             employee_id=employee_id,
#             date=date,
#             clock_in_time=clock_in_time,
#             clock_out_time=clock_out_time
#         )
#         data_dict = jsonable_encoder(item_data)
#         inserted_id = insert_item(attendance_collection, data_dict)
#         return RedirectResponse(
#             "/web/attendance", status_code=302
#         )
#
#     return templates.TemplateResponse("admin/create.html", context=locals())