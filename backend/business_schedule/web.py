import uuid
from datetime import time, datetime
from fastapi import Request, Form
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from typing import Optional
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException

from .helpers import jinja_variables_for_business_schedule
from .schema import RegisterBusinessSchedule, UpdateBusinessSchedule
from ..queries import insert_item, get_item, update_item, delete_item, filter_data
from ..forms import BusinessScheduleForm
from ..utils import prepare_dropdown_for_forms

router = APIRouter()
templates = Jinja2Templates(directory=r"templates")
business_schedule_collection = 'business_schedule'


@router.get("/business_schedule", response_class=HTMLResponse)
async def business_schedule(request: Request) -> HTMLResponse:
    columns, data, name, table_name = jinja_variables_for_business_schedule()
    modify = True
    return templates.TemplateResponse("admin/index.html", context=locals())


@router.get("/business_schedule/new", response_class=HTMLResponse)
def show_add_business_schedule_form(request: Request) -> HTMLResponse:
    form = BusinessScheduleForm(request)
    name = "Business Schedule"
    return templates.TemplateResponse("admin/create.html", context=locals())


@router.post("/business_schedule/new", response_class=HTMLResponse)
async def save_business_form(
    request: Request,
    merchant_id: str = Form(...),
    day_of_week: str = Form(...),
    opening_time: time = Form(...),
    closing_time: time = Form(...)
) -> Response:
    form = BusinessScheduleForm(request=request)
    form.merchant_id.data = merchant_id
    form.day_of_week.data = day_of_week
    form.opening_time.data = opening_time
    form.closing_time.data = closing_time

    if await form.validate():
        business_data = RegisterBusinessSchedule(
            merchant_id=merchant_id,
            day_of_week=day_of_week,
            opening_time=opening_time,
            closing_time=closing_time
        )
        business_data_dict = jsonable_encoder(business_data)
        insert_item(business_schedule_collection, business_data_dict)
        return RedirectResponse(
            "/web/business_schedule", status_code=302
        )

    return templates.TemplateResponse("admin/create.html", context=locals())


@router.get("/business_schedule/update/{item_id}", response_class=HTMLResponse)
def show_business_schedule_update_form(request: Request, item_id: str) -> HTMLResponse:
    obj = get_item(business_schedule_collection, item_id=item_id)
    obj = obj['data']
    dict_data = {
        "merchant_id": obj.get("merchant_id", "-"),
        "day_of_week": obj.get("day_of_week", "-"),
        "opening_time": datetime.strptime(
            obj['opening_time'],
            "%H:%M:%S"
        ).time() if obj.get("opening_time", "-") else "-",
        "closing_time": datetime.strptime(
            obj["closing_time"],
            "%H:%M:%S"
        ).time() if obj.get("closing_time", "-") else "-"
    }
    form = BusinessScheduleForm(request=request, data=dict_data)
    name = "Business Schedule"
    return templates.TemplateResponse("admin/update.html", context=locals())


@router.post("/business_schedule/update/{item_id}", response_class=HTMLResponse)
async def save_business_schedule_update_form(
    request: Request,
    item_id: str,
    merchant_id: str = Form(...),
    day_of_week: str = Form(...),
    opening_time: time = Form(...),
    closing_time: time = Form(...)
) -> Response:
    form = BusinessScheduleForm(request=request)
    form.business_schedule_id.data = item_id
    form.merchant_id.data = merchant_id
    form.day_of_week.data = day_of_week
    form.opening_time.data = opening_time
    form.closing_time.data = closing_time

    if await form.validate():
        update_data = UpdateBusinessSchedule(
            merchant_id=merchant_id,
            day_of_week=day_of_week,
            opening_time=opening_time,
            closing_time=closing_time,
        )
        business_data_dict = jsonable_encoder(update_data)
        update_item(business_schedule_collection, item_id, business_data_dict)
        return RedirectResponse(
            "/web/business_schedule", status_code=302
        )

    return templates.TemplateResponse("admin/update.html", context=locals())


@router.get("/business_schedule/delete/{item_id}", response_class=HTMLResponse)
def save_business_schedule_update_form(item_id: str) -> RedirectResponse:
    delete_item(business_schedule_collection, item_id)
    return RedirectResponse(
        "/web/business_schedule", status_code=302
    )
