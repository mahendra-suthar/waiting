import re
from fastapi import Request, Form
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from typing import Optional
from fastapi.encoders import jsonable_encoder

from .helpers import jinja_variables_for_business
from .schema import RegisterBusiness, UpdateBusiness
from ..forms import BusinessForm, BusinessScheduleForm
from ..queries import insert_item, get_item, update_item, delete_item
from ..constants import MERCHANT
from ..utils import prepare_dropdown_for_forms

router = APIRouter()
templates = Jinja2Templates(directory=r"templates")
business_collection = 'business'
user_collection = 'users'
category_collection = 'category'


@router.get("/business", response_class=HTMLResponse)
async def users(request: Request) -> HTMLResponse:
    columns, data, name, table_name = jinja_variables_for_business()
    modify = True
    return templates.TemplateResponse("admin/index.html", context=locals())


@router.get("/business/new", response_class=HTMLResponse)
def show_add_business_form(request: Request) -> HTMLResponse:
    form = BusinessForm(request)
    form.category_id.choices = prepare_dropdown_for_forms(
            collection_name=category_collection,
            label='name',
            value='_id'
        )
    # form = BusinessScheduleForm(request)
    name = "Business"
    return templates.TemplateResponse("admin/create.html", context=locals())


@router.post("/business/new", response_class=HTMLResponse)
async def save_business_form(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    country_code: str = Form(...),
    phone_number: str = Form(...),
    address_id: Optional[str] = Form(None),
    about_business: Optional[str] = Form(None),
    category_id: str = Form(...),
    owner_id: str = Form(...)
) -> Response:
    form = BusinessForm(request=request)
    form.name.data = name
    form.email.data = email
    form.password.data = password
    form.country_code.data = country_code
    form.phone_number.data = phone_number
    form.address_id.data = address_id
    form.about_business.data = about_business
    form.category_id.data = category_id
    form.owner_id.data = owner_id

    if await form.validate():
        business_data = RegisterBusiness(
            name=name,
            email=email,
            password=password,
            country_code=country_code,
            phone_number=phone_number,
            address_id=address_id,
            about_business=about_business,
            category_id=category_id,
            status=1,
            owner_id=owner_id
        )
        business_data_dict = jsonable_encoder(business_data)
        inserted_id = insert_item(business_collection, business_data_dict)
        if inserted_id and owner_id:
            update_item(user_collection, owner_id, {'user_type': MERCHANT})
        return RedirectResponse(
            "/web/business", status_code=302
        )

    return templates.TemplateResponse("admin/create.html", context=locals())


@router.get("/business/update/{item_id}", response_class=HTMLResponse)
def show_business_update_form(request: Request, item_id: str) -> HTMLResponse:
    obj = get_item(business_collection, item_id=item_id)
    obj = obj['data']
    dict_data = {
        "name": obj["name"],
        "email": obj["email"],
        "password": obj["password"],
        "country_code": obj["country_code"],
        "phone_number": obj["phone_number"],
        "address_id": obj["address_id"],
        "about_business": obj["about_business"],
        "category_id": obj["category_id"],
    }
    form = BusinessForm(request=request, data=dict_data)
    name = "Business"
    return templates.TemplateResponse("admin/update.html", context=locals())


@router.post("/business/update/{item_id}", response_class=HTMLResponse)
async def save_business_update_form(
    request: Request,
    item_id: str,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    country_code: str = Form(...),
    phone_number: str = Form(...),
    address_id: Optional[str] = Form(None),
    about_business: Optional[str] = Form(None),
    category_id: str = Form(...)
) -> Response:
    form = BusinessForm(request=request)
    form.business_id.data = item_id
    form.name.data = name
    form.email.data = email
    form.password.data = password
    form.country_code.data = country_code
    form.phone_number.data = phone_number
    form.address_id.data = address_id
    form.about_business.data = about_business
    form.category_id.data = category_id

    if await form.validate():
        update_data = UpdateBusiness(
            name=name,
            email=email,
            password=password,
            country_code=country_code,
            phone_number=phone_number,
            address_id=address_id,
            about_business=about_business,
            category_id=category_id,
        )
        business_data_dict = jsonable_encoder(update_data)
        update_item(business_collection, item_id, business_data_dict)
        return RedirectResponse(
            "/web/business", status_code=302
        )

    return templates.TemplateResponse("admin/update.html", context=locals())


@router.get("/business/delete/{item_id}", response_class=HTMLResponse)
def save_business_update_form(item_id: str) -> RedirectResponse:
    delete_item(business_collection, item_id)
    return RedirectResponse(
        "/web/business", status_code=302
    )