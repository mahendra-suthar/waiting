from datetime import time
from fastapi import Request, Form
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, Response, RedirectResponse
from typing import Optional
from fastapi.encoders import jsonable_encoder

from .helpers import jinja_variables_for_queue
from ..forms import QueueForm
from .schema import RegisterQueue
from ..queries import insert_item, update_item, delete_item, get_item

router = APIRouter()
templates = Jinja2Templates(directory=r"templates")
queue_collection = 'queue'


@router.get("/queue", response_class=HTMLResponse)
async def get_queue(request: Request) -> HTMLResponse:
    columns, data, name, table_name = jinja_variables_for_queue()
    modify = True
    return templates.TemplateResponse("admin/index.html", context=locals())


@router.get("/queue/new", response_class=HTMLResponse)
def show_add_queue_form(request: Request) -> HTMLResponse:
    form = QueueForm(request)
    name = "Queue"
    return templates.TemplateResponse("admin/create.html", context=locals())


@router.post("/queue/new", response_class=HTMLResponse)
async def save_queue_form(
    request: Request,
    name: str = Form(...),
    merchant_id: str = Form(...),
    employee_id: str = Form(...),
    limit: int = Form(...),
    start_time: time = Form(...),
    end_time: time = Form(...),
) -> Response:
    form = QueueForm(request=request)
    form.name.data = name
    form.merchant_id.data = merchant_id
    form.employee_id.data = employee_id
    form.limit.data = limit
    form.start_time.data = start_time
    form.end_time.data = end_time

    if await form.validate():
        item_data = RegisterQueue(
            name=name,
            merchant_id=merchant_id,
            employee_id=employee_id,
            limit=limit,
            start_time=start_time,
            end_time=end_time
        )
        data_dict = jsonable_encoder(item_data)
        insert_item(queue_collection, data_dict)
        return RedirectResponse(
            "/web/queue", status_code=302
        )

    return templates.TemplateResponse("admin/create.html", context=locals())


@router.get("/queue/delete/{item_id}", response_class=HTMLResponse)
def save_queue_update_form(item_id: str) -> RedirectResponse:
    delete_item(queue_collection, item_id)
    return RedirectResponse(
        "/web/queue", status_code=302
    )