from fastapi import HTTPException, status
from bson import ObjectId
from typing import Any

from ..queries import insert_item, update_item, get_item, get_item_list, filter_data, prepare_item_list
from .schema import UserData

user_collection = 'users'


async def insert_user_request(user_dict: dict, created_by: str = None) -> str:
    """
    Add user
    """

    is_email_exist = filter_data(user_collection, filter_dict={'email': user_dict.get("email")})
    if is_email_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exist")

    is_phone_exist = filter_data(user_collection, filter_dict={'phone_number': user_dict.get("phone_number")})
    if is_phone_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Phone Number already exist")
    res_data = insert_item(user_collection, item_data=user_dict, created_by=created_by)
    return res_data


async def update_user_request(user_id: str, user_dict: dict) -> Any:
    """
    Update user
    """
    is_user_exist = filter_data(user_collection, filter_dict={'_id': ObjectId(user_id)})
    if not is_user_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found with this Id")

    is_email_exist = filter_data(
        user_collection,
        filter_dict={'_id': {'$ne': ObjectId(user_id)}, 'email': user_dict.get("email")}
    )
    if is_email_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exist")

    is_phone_exist = filter_data(
        user_collection,
        filter_dict={'_id': {'$ne': ObjectId(user_id)}, 'phone_number': user_dict.get("phone_number")}
    )
    if is_phone_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Phone Number already exist")

    response_data = await update_item(user_collection, item_id=user_id, item_data=user_dict)
    return response_data


def get_user_by_id(user_id: str) -> Any:
    """
    Update user
    """
    is_user_exist = filter_data(user_collection, filter_dict={'_id': ObjectId(user_id)})
    if not is_user_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found with this Id")

    response_data = get_item(user_collection, item_id=user_id)
    return response_data


def get_users_list() -> Any:
    """
    Update user
    """
    response_data = get_item_list(user_collection, columns=['_id', 'full_name', 'phone_number', 'email'])
    return response_data


def jinja_variables_for_user():
    data_dict = {
        'collection_name': user_collection,
        'schema': UserData
    }
    columns = list(UserData.__annotations__.keys())
    data = prepare_item_list(data_dict)
    table_name = user_collection
    name = 'User'
    return columns, data, name, table_name


