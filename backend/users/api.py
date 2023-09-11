from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import Body, HTTPException
from fastapi.routing import APIRouter
from pymongo.errors import WriteError

from logs import logger as log
from models.users import User
from .schema import RegisterUser
from .helpers import insert_user
from ..utils import success_response


router = APIRouter()


@router.post("/v1/user", response_description="Add new User", response_model=User)
async def create_user(user: RegisterUser = Body(...)):
    """
    Register user api
    """
    try:
        user = jsonable_encoder(user)
        inserted_user = insert_user(user)
        response_data = success_response(data={'user_id': str(inserted_user)}, message="Successfully inserted data")
        return JSONResponse(content=response_data, status_code=201)
    except Exception as e:
        log.error(f"Error while creating a user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")



