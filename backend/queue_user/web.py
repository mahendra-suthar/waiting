from fastapi import Request, Form
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, Response, RedirectResponse
from typing import Optional
from fastapi.encoders import jsonable_encoder

from .helpers import jinja_variables_for_queue_user
from ..forms import QueueUserForm
from .schema import RegisterQueueUser
from ..queries import insert_item, update_item, delete_item, get_item

router = APIRouter()
templates = Jinja2Templates(directory=r"templates")
queue_user_collection = 'queue_user'


@router.get("/queue_user", response_class=HTMLResponse)
async def get_all_queue_users(request: Request) -> HTMLResponse:
    columns, data, name, table_name = jinja_variables_for_queue_user()
    modify = True
    return templates.TemplateResponse("admin/index.html", context=locals())


@router.get("/queue_user/new", response_class=HTMLResponse)
def show_add_queue_user_form(request: Request) -> HTMLResponse:
    form = QueueUserForm(request)
    name = "Queue User"
    return templates.TemplateResponse("admin/create.html", context=locals())


@router.post("/queue_user/new", response_class=HTMLResponse)
async def save_queue_form(
    request: Request,
    user_id: str = Form(...),
    queue_id: str = Form(...),
    priority: bool = Form(False),
    enqueue_time: Optional[int] = Form(0),
    dequeue_time: Optional[int] = Form(0),
) -> Response:
    form = QueueUserForm(request=request)
    form.user_id.data = user_id
    form.queue_id.data = queue_id
    form.priority.data = priority
    form.enqueue_time.data = enqueue_time
    form.dequeue_time.data = dequeue_time

    if await form.validate():
        item_data = RegisterQueueUser(
            user_id=user_id,
            queue_id=queue_id,
            priority=priority,
            enqueue_time=enqueue_time,
            dequeue_time=dequeue_time
        )
        data_dict = jsonable_encoder(item_data)
        insert_item(queue_user_collection, data_dict)
        return RedirectResponse(
            "/web/queue_user", status_code=302
        )

    return templates.TemplateResponse("admin/create.html", context=locals())