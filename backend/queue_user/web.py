from fastapi import Request, Form, HTTPException
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, Response, RedirectResponse
from typing import Optional
from fastapi.encoders import jsonable_encoder

from .helpers import jinja_variables_for_queue_user, update_queue
from ..forms import QueueUserForm
from .schema import RegisterQueueUser, UpdateQueueUser
from ..queries import insert_item, filter_data
from ..utils import get_current_timestamp_utc, get_current_date_str
from ..constants import QUEUE_USER_REGISTERED, QUEUE_USER_IN_PROGRESS


router = APIRouter()
templates = Jinja2Templates(directory=r"templates")
queue_user_collection = 'queue_user'
queue_collection = 'queue'


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


# @router.post("/queue_user/new", response_class=HTMLResponse)
# async def save_queue_form(
#     request: Request,
#     user_id: str = Form(...),
#     queue_id: str = Form(...),
#     priority: bool = Form(False),
#     enqueue_time: Optional[int] = Form(0),
#     dequeue_time: Optional[int] = Form(0),
# ) -> Response:
#     form = QueueUserForm(request=request)
#     form.user_id.data = user_id
#     form.queue_id.data = queue_id
#     form.priority.data = priority
#     form.enqueue_time.data = enqueue_time
#     form.dequeue_time.data = dequeue_time
#
#     if await form.validate():
#         item_data = RegisterQueueUser(
#             user_id=user_id,
#             queue_id=queue_id,
#             priority=priority,
#             enqueue_time=get_current_timestamp_utc(),
#             dequeue_time=dequeue_time
#         )
#         data_dict = jsonable_encoder(item_data)
#         insert_item(queue_user_collection, data_dict)
#         return RedirectResponse(
#             "/web/queue_user", status_code=302
#         )
#
#     return templates.TemplateResponse("admin/create.html", context=locals())


@router.post("/queue_user/new", response_class=HTMLResponse)
async def save_queue_form(
    request: Request,
    user_id: str = Form(...),
    queue_id: str = Form(...),
    queue_date: Optional[int] = Form(0),
    priority: bool = Form(False),
    enqueue_time: Optional[int] = Form(0),
    dequeue_time: Optional[int] = Form(0),
) -> Response:
    form = QueueUserForm(request=request)
    form.user_id.data = user_id
    form.queue_id.data = queue_id
    form.queue_date.data = queue_date
    form.priority.data = priority
    form.enqueue_time.data = enqueue_time
    form.dequeue_time.data = dequeue_time

    if await form.validate():

        item_data = RegisterQueueUser(
            user_id=user_id,
            queue_id=queue_id,
            queue_date=queue_date,
            priority=priority,
            enqueue_time=get_current_timestamp_utc(),
            dequeue_time=dequeue_time,
            service_id=None,
            employee_id=None
        )
        print("item_data", item_data)
        data_dict = jsonable_encoder(item_data)
        if queue_id and user_id:
            q_user_obj = filter_data(
                collection_name='queue_user',
                filter_dict={
                    'status': {'$in': [int(QUEUE_USER_REGISTERED), int(QUEUE_USER_IN_PROGRESS)]},
                    'user_id': user_id, 'queue_id': queue_id
                }
            )
            print("q_user_obj", q_user_obj)
            if q_user_obj:
                raise HTTPException(status_code=400, detail="Data already exists")
        inserted_id = insert_item(queue_user_collection, data_dict)
        date_str = get_current_date_str(queue_date)
        update_queue(str(user_id), queue_id, date_str)
        return RedirectResponse(
            "/web/queue_user", status_code=302
        )

    return templates.TemplateResponse("admin/create.html", context=locals())


# @router.post("/queue_user/update/{item_id}", response_class=HTMLResponse)
# async def save_queue_user_update_form(
#     request: Request,
#     item_id: str,
#     user_id: str = Form(...),
#     queue_id: str = Form(...),
#     enqueue_time: Optional[int] = get_current_timestamp_utc(),
#     dequeue_time: Optional[int] = Form(None),
#     status: int:
#     priority: bool
#     merchant_id: str = Form(...),
#     email: str = Form(...),
#     country_code: str = Form(...),
#     phone_number: str = Form(...),
#     joined_date: Optional[int] = Form(None),
#     department_id: Optional[str] = Form(None),
#     employee_number: Optional[int] = Form(None)
# ) -> RedirectResponse:
#     name = 'Employee'
#
#     form = QueueUserForm(request=request)
#     form.employee_id.data = item_id
#     form.merchant_id.data = merchant_id
#     form.email.data = email
#     form.country_code.data = country_code
#     form.phone_number.data = phone_number
#     form.joined_date.data = joined_date
#     form.department_id.data = department_id
#     form.employee_number.data = employee_number
#
#     if await form.validate():
#         item_data = UpdateQueueUser(
#             merchant_id=merchant_id,
#             email=email,
#             country_code=country_code,
#             phone_number=phone_number,
#             joined_date=joined_date,
#             department_id=department_id,
#             employee_number=employee_number,
#         )
#
#         data_dict = jsonable_encoder(item_data)
#         update_item(queue_user_collection, item_id, data_dict)
#         return RedirectResponse(
#             "/web/queue_user", status_code=302
#         )
#
#     return templates.TemplateResponse("admin/update.html", context=locals())