from fastapi import Request, Form, UploadFile, File
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, Response, RedirectResponse
from fastapi.encoders import jsonable_encoder

from .helpers import jinja_variables_for_post_service, save_uploaded_file
from ..forms import PostForm
from ..utils import prepare_dropdown_for_forms, prepare_static_choice_dropdown
from ..queries import insert_item
from ..constants import post_type_choices
from .schema import RegisterPost


router = APIRouter()
templates = Jinja2Templates(directory=r"templates")
post_collection = 'post'
business_collection = 'business'


@router.get("/post", response_class=HTMLResponse)
async def get_all_post(request: Request) -> HTMLResponse:
    columns, data, name, table_name = jinja_variables_for_post_service()
    modify = True
    return templates.TemplateResponse("admin/index.html", context=locals())


@router.get("/post/new", response_class=HTMLResponse)
def show_add_post_form(request: Request) -> HTMLResponse:
    form = PostForm(request)
    form.business_id.choices = prepare_dropdown_for_forms(collection_name=business_collection, label='name', value='_id')
    form.post_type.choices = prepare_static_choice_dropdown(post_type_choices)
    name = "Post"
    return templates.TemplateResponse("admin/create.html", context=locals())


@router.post("/post/new", response_class=HTMLResponse)
async def save_post_form(
    request: Request,
    business_id: str = Form(...),
    title: str = Form(...),
    image: UploadFile = File(...),
    content: str = Form(...),
    post_type: str = Form(...)
) -> Response:
    form = PostForm(request=request)
    form.business_id.choices = prepare_dropdown_for_forms(collection_name=business_collection, label='name', value='_id')
    form.post_type.choices = prepare_static_choice_dropdown(post_type_choices)

    form.business_id.data = business_id
    form.title.data = title
    form.image.data = image
    form.content.data = content
    form.post_type.data = post_type

    if await form.validate():
        image_path = await save_uploaded_file(image)
        item_data = RegisterPost(
            business_id=business_id,
            title=title,
            image=image_path,
            content=content,
            post_type=post_type
        )
        data_dict = jsonable_encoder(item_data)
        insert_item(post_collection, data_dict)
        return RedirectResponse(
            "/web/post", status_code=302
        )

    return templates.TemplateResponse("admin/create.html", context=locals())