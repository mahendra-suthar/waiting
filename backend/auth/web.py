from fastapi import Request, Form, UploadFile, File, Response, HTTPException
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.encoders import jsonable_encoder


from ..forms import LoginForm
from ..queries import filter_data
from ..utils import verify_password, save_cookies
from ..auth.helpers import create_jwt_token

router = APIRouter()
templates = Jinja2Templates(directory=r"templates")
business_collection = 'business'
user_collection = 'users'
category_collection = 'category'


@router.get("/login", response_class=HTMLResponse)
async def login(request: Request) -> HTMLResponse:
    form = LoginForm(request)
    return templates.TemplateResponse("admin/create.html", context=locals())


@router.post("/login", response_class=HTMLResponse)
async def get_login(
        request: Request,
        response: Response,
        email: str = Form(...),
        password: str = Form(...)
) -> HTMLResponse:
    form = LoginForm(request=request)
    form.email.data = email
    form.password.data = password

    if await form.validate():
        check_email = filter_data(user_collection, {'email': email})
        if check_email:
            check_password = verify_password(password, check_email['password'])
            if check_password:
                token = create_jwt_token(check_email['_id'])
                save_cookies(response, 'access_token', token)
                # return templates.TemplateResponse("admin/.html", context=locals())
            else:
                raise HTTPException(status_code=400, detail="Password not match")
        else:
            raise HTTPException(status_code=400, detail="Email not found")

    return templates.TemplateResponse("admin/create.html", context=locals())