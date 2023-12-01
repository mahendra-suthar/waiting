from fastapi import Request, Form
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, Response, RedirectResponse
from typing import Optional
from fastapi.encoders import jsonable_encoder

# from ..web_helpers import jinja_variables_for_users
from .helpers import jinja_variables_for_user
from ..forms import UsersForm
from .schema import RegisterUser, UpdateUser
from ..queries import insert_item, update_item, delete_item, get_item

router = APIRouter()
templates = Jinja2Templates(directory=r"templates")
users_collection = 'users'


@router.get("/user", response_class=HTMLResponse)
async def users(request: Request) -> HTMLResponse:
    columns, data, name, table_name = jinja_variables_for_user()
    modify = True
    return templates.TemplateResponse("admin/index.html", context=locals())


@router.get("/users/new", response_class=HTMLResponse)
def show_add_users_form(request: Request) -> HTMLResponse:
    form = UsersForm(request)
    name = "User"
    return templates.TemplateResponse("admin/create.html", context=locals())


@router.post("/users/new", response_class=HTMLResponse)
async def save_users_form(
    request: Request,
    first_name: Optional[str] = Form(None),
    last_name: Optional[str] = Form(None),
    full_name: str = Form(...),
    phone_number: str = Form(...),
    email: str = Form(...),
    date_of_birth: Optional[int] = Form(None),
) -> Response:
    name = "User"

    form = UsersForm(request=request)
    form.first_name.data = first_name
    form.last_name.data = last_name
    form.full_name.data = full_name
    form.phone_number.data = phone_number
    form.email.data = email
    form.date_of_birth.data = date_of_birth

    if await form.validate():
        item_data = RegisterUser(
            first_name=first_name,
            last_name=last_name,
            full_name=full_name,
            phone_number=phone_number,
            email=email,
            date_of_birth=date_of_birth,
        )
        data_dict = jsonable_encoder(item_data)
        insert_item(users_collection, data_dict)
        return RedirectResponse(
            "/web/user", status_code=302
        )

    return templates.TemplateResponse("admin/create.html", context=locals())


@router.get("/user/update/{item_id}", response_class=HTMLResponse)
def show_users_update_form(request: Request, item_id: str) -> HTMLResponse:
    obj = get_item(users_collection, item_id=item_id)
    obj = obj['data']
    dict_data = {
        "first_name": obj['first_name'],
        "last_name": obj['last_name'],
        "full_name": obj['full_name'],
        "phone_number": obj['phone_number'],
        "email": obj['email'],
        "date_of_birth": obj['date_of_birth'],
    }
    form = UsersForm(request=request, data=dict_data)
    name = "Users"
    return templates.TemplateResponse("admin/update.html", context=locals())


@router.post("/user/update/{item_id}", response_class=HTMLResponse)
async def save_user_update_form(
    request: Request,
    item_id: str,
    first_name: Optional[str] = Form(None),
    last_name: Optional[str] = Form(None),
    full_name: str = Form(...),
    phone_number: str = Form(...),
    email: str = Form(...),
    date_of_birth: Optional[int] = Form(None),
) -> Response:
    name = "User"

    form = UsersForm(request=request)
    form.first_name.data = first_name
    form.last_name.data = last_name
    form.full_name.data = full_name
    form.phone_number.data = phone_number
    form.email.data = email
    form.date_of_birth.data = date_of_birth

    if await form.validate():
        update_data = UpdateUser(
            first_name=first_name,
            last_name=last_name,
            full_name=full_name,
            phone_number=phone_number,
            email=email,
            date_of_birth=date_of_birth,
        )
        data_dict = jsonable_encoder(update_data)
        update_item(users_collection, item_id, data_dict)
        return RedirectResponse(
            "/web/user", status_code=302
        )

    return templates.TemplateResponse("admin/update.html", context=locals())


@router.get("/user/delete/{item_id}", response_class=HTMLResponse)
def save_user_update_form(item_id: str) -> RedirectResponse:
    delete_item(users_collection, item_id)
    return RedirectResponse(
        "/web/user", status_code=302
    )