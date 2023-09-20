from fastapi import Request
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from ..web_helpers import jinja_variables_for_users

router = APIRouter()
templates = Jinja2Templates(directory=r"templates")


@router.get("/users", response_class=HTMLResponse)
async def users(request: Request) -> HTMLResponse:
    columns, data, name, table_name = jinja_variables_for_users()
    return templates.TemplateResponse("admin/index.html", context=locals())
