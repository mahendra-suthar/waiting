from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import Body, HTTPException
from fastapi.routing import APIRouter
from typing import Any

from logs import logger as log
from models.users import User
from .schema import RegisterUser, UpdateUser
from .helpers import insert_user_request, update_user_request, get_user_by_id, get_users_list
from ..utils import success_response, error_response
from ..queries import update_item
from config.database import client_db


router = APIRouter()


@router.post("/v1/user", response_description="Add new User", response_model=User)
async def create_user(user: RegisterUser = Body(...)) -> Any:
    """
    Register user api
    """
    try:
        user_data = jsonable_encoder(user)
        inserted_user = insert_user_request(user_data)
        response_data = success_response(data={'user_id': str(inserted_user)}, message="Successfully inserted data")
        return JSONResponse(content=response_data, status_code=201)
    except Exception as e:
        log.error(f"Error while creating a user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/v1/user/{user_id}", response_description="Update User Profile", response_model=User)
async def update_user(user_id: str, user: UpdateUser = Body(...)) -> Any:
    """
    Update User Profile
    """
    try:
        user_data = jsonable_encoder(user)
        response_data = update_user_request(user_id, user_data)
        status_code = response_data.get("status")
        return JSONResponse(content=response_data, status_code=status_code)
    except Exception as e:
        log.error(f"Error while creating a user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/v1/user/{user_id}", response_description="Get User Profile", response_model=User)
async def get_user(user_id: str) -> Any:
    """
    Get User Profile
    """
    try:
        response_data = get_user_by_id(user_id)
        status_code = response_data.get("status")
        return JSONResponse(content=response_data, status_code=status_code)
    except Exception as e:
        log.error(f"Error while creating a user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/v1/users", response_description="Get all users", response_model=User)
async def get_users() -> Any:
    """
    Get all Users
    """
    try:
        response_data = get_users_list()
        status_code = response_data.get("status")
        return JSONResponse(content=response_data, status_code=status_code)
    except Exception as e:
        log.error(f"Error while creating a user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")



