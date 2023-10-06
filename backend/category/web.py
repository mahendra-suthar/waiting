import uuid

from fastapi import Request, Form
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Optional
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException

from .helpers import jinja_variables_for_category
from .schema import RegisterCategory, UpdateCategory
from ..queries import insert_item, get_item, update_item, delete_item, filter_data
from ..forms import CategoryForm
from ..utils import prepare_dropdown_for_forms

router = APIRouter()
templates = Jinja2Templates(directory=r"templates")
category_collection = 'category'


@router.get("/category", response_class=HTMLResponse)
async def categories(request: Request) -> HTMLResponse:
    columns, data, name, table_name = jinja_variables_for_category()
    modify = True
    return templates.TemplateResponse("admin/index.html", context=locals())


@router.get("/category/new", response_class=HTMLResponse)
def show_add_category_form(request: Request) -> HTMLResponse:
    form = CategoryForm(request)
    name = "Category"
    return templates.TemplateResponse("admin/create.html", context=locals())


@router.get("/category/update/{item_id}", response_class=HTMLResponse)
def show_category_update_form(request: Request, item_id: str) -> HTMLResponse:
    obj = get_item(collection_name='category', item_id=item_id)
    obj = obj['data']
    dict_data = {
        'name': obj['name'],
        'description': obj['description'],
        'parent_category_id': obj['parent_category_id']
    }
    form = CategoryForm(request=request, data=dict_data)
    name = "Category"
    return templates.TemplateResponse("admin/update.html", context=locals())


@router.post("/category/new", response_class=HTMLResponse)
def save_category_form(
    request: Request,
    name: str = Form(...),
    description: str = Form(''),
    parent_category_id: Optional[str] = Form(None),
) -> RedirectResponse:
    error_message = {}

    if filter_data(category_collection, {'name': name}):
        error_message['Name'] = "Category Name already exists"

    if error_message:
        dict_data = {
            'name': name,
            'description': description,
            'parent_category_id': parent_category_id
        }
        form = CategoryForm(request=request, data=dict_data)
        return templates.TemplateResponse("admin/create.html", context=locals())

    category_data = RegisterCategory(
        name=name,
        description=description,
        parent_category_id=parent_category_id,
    )
    category_data_dict = jsonable_encoder(category_data)
    insert_item(category_collection, category_data_dict)
    return RedirectResponse(
        "/web/category", status_code=302
    )


@router.post("/category/update/{item_id}", response_class=HTMLResponse)
def save_category_update_form(
    item_id: str,
    name: str = Form(...),
    description: str = Form(''),
    parent_category_id: Optional[str] = Form(None),
) -> RedirectResponse:
    category_data = UpdateCategory(
        name=name,
        description=description,
        parent_category_id=parent_category_id,
    )

    category_data_dict = jsonable_encoder(category_data)
    update_item(category_collection, item_id, category_data_dict)
    return RedirectResponse(
        "/web/category", status_code=302
    )


@router.get("/category/delete/{item_id}", response_class=HTMLResponse)
def save_category_update_form(item_id: str) -> RedirectResponse:
    delete_item(category_collection, item_id)
    return RedirectResponse(
        "/web/category", status_code=302
    )
