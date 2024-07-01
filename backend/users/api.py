from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import Body, Depends, status
from fastapi.routing import APIRouter
from typing import Any
from fastapi.exceptions import HTTPException
from bson import ObjectId

from models.users import User
from .schema import RegisterUser, UpdateUser, UpdateUserProfile
from .helpers import insert_user_request, update_user_request, get_user_by_id, get_users_list
from ..utils import success_response, error_response, prepare_dropdown_data
from ..auth.helpers import get_current_user, JWTBearer
from ..queries import update_item, filter_data


router = APIRouter()
users_collection = 'users'


@router.post("/v1/user",
             response_description="Add new User",
             response_model=User,
             dependencies=[])
async def create_user(user: RegisterUser = Body(...)) -> Any:
    """
    Register user api
    """
    user_data = jsonable_encoder(user)
    inserted_user = await insert_user_request(user_data)
    response_data = success_response(data={'user_id': str(inserted_user)}, message="Successfully inserted data")
    return JSONResponse(content=response_data, status_code=201)


@router.put("/v1/user/{user_id}", response_description="Update User Profile", response_model=User)
async def update_user(user_id: str, user: UpdateUser = Body(...), current_user: str = Depends(JWTBearer())) -> Any:
    """
    Update User Profile
    """
    user_data = jsonable_encoder(user)
    user_data['updated_by'] = current_user
    response_data = await update_user_request(user_id, user_data)
    status_code = response_data.get("status")
    return JSONResponse(content=response_data, status_code=status_code)


# @router.patch("/v1/user/{user_id}", response_description="Update User Profile", response_model=User)
# async def partial_update_user(user_id: str, user: UpdateUser = Body(...)) -> Any:
#     """
#     Update User Profile
#     """
#     user_data = jsonable_encoder(user)
#     response_data = await update_user_request(user_id, user_data)
#     status_code = response_data.get("status")
#     return JSONResponse(content=response_data, status_code=status_code)


@router.get("/v1/user/{user_id}",
            response_description="Get User details",
            response_model=User,
            dependencies=[Depends(JWTBearer())])
async def get_user(user_id: str) -> Any:
    """
    Get User details
    """
    response_data = get_user_by_id(user_id)
    status_code = response_data.get("status")
    return JSONResponse(content=response_data, status_code=status_code)


@router.get("/v1/users",
            response_description="Get all users",
            response_model=User,
            dependencies=[Depends(JWTBearer())])
async def get_users() -> Any:
    """
    Get all Users
    """
    response_data = get_users_list()
    status_code = response_data.get("status")
    return JSONResponse(content=response_data, status_code=status_code)


@router.get("/v1/user_profile",
            response_description="get user profile details",
            response_model=User)
async def user_profile(current_user: str = Depends(JWTBearer())):
    """
    Get User Profile details
    """
    response_data = get_user_by_id(current_user)
    status_code = response_data.get("status")
    return JSONResponse(content=response_data, status_code=status_code)


@router.put("/v1/update_user_profile",
            response_description="update user profile details",
            response_model=User)
async def update_user_profile(current_user: str = Depends(JWTBearer()), user: UpdateUserProfile = Body(...)):
    """
    update User Profile details
    """
    data_dict = jsonable_encoder(user)
    existing_email = filter_data(users_collection, {
        'email': data_dict.get("email"),
        '_id': {"$ne": ObjectId(current_user)}
    })
    if existing_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exist")

    existing_phone = filter_data(users_collection, {
        'phone_number': data_dict.get("phone_number"),
        '_id': {"$ne": ObjectId(current_user)}
    })
    if existing_phone:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Phone Number already exist")

    response_data = update_item(users_collection, current_user, data_dict, current_user)
    status_code = response_data.get("status")
    return JSONResponse(content=response_data, status_code=status_code)


@router.get("/v1/user_dropdown_data",
            response_description="get user dropdown data",
            response_model=User,
            dependencies=[Depends(JWTBearer())])
async def user_dropdown():
    """
    get user dropdown data
    """
    data_list = prepare_dropdown_data(collection_name='user', label='full_name', value='_id')
    response_data = success_response(data=data_list, message="Successfully get data")
    status_code = response_data.get("status")
    return JSONResponse(content=response_data, status_code=status_code)


