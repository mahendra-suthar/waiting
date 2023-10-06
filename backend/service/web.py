from fastapi import Request, Form
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, Response, RedirectResponse
from typing import Optional
from fastapi.encoders import jsonable_encoder

from .helpers import jinja_variables_for_service
from ..forms import ServiceForm
from .schema import RegisterService
from ..queries import insert_item, update_item, delete_item, get_item

router = APIRouter()
templates = Jinja2Templates(directory=r"templates")
service_collection = 'service'


@router.get("/service", response_class=HTMLResponse)
async def get_service(request: Request) -> HTMLResponse:
    columns, data, name, table_name = jinja_variables_for_service()
    modify = True
    return templates.TemplateResponse("admin/index.html", context=locals())


@router.get("/service/new", response_class=HTMLResponse)
def show_add_service_form(request: Request) -> HTMLResponse:
    form = ServiceForm(request)
    name = "Service"
    return templates.TemplateResponse("admin/create.html", context=locals())


@router.post("/service/new", response_class=HTMLResponse)
async def save_queue_form(
    request: Request,
    name: str = Form(...),
    merchant_id: str = Form(...),
    description: Optional[str] = Form('')
) -> Response:
    form = ServiceForm(request=request)
    form.name.data = name
    form.merchant_id.data = merchant_id
    form.description.data = description

    if await form.validate():
        item_data = RegisterService(
            name=name,
            description=description,
            merchant_id=merchant_id,
        )
        data_dict = jsonable_encoder(item_data)
        insert_item(service_collection, data_dict)
        return RedirectResponse(
            "/web/service", status_code=302
        )

    return templates.TemplateResponse("admin/create.html", context=locals())