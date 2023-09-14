import pymongo
from fastapi import HTTPException, status
from pymongo.errors import WriteError
from typing import Any

from logs import logger as log
from config.database import client_db
from ..queries import insert_item, update_item, get_item, get_item_list, filter_data

user_collection = client_db['users']
# user_collection.create_index([("email", pymongo.ASCENDING), ("phone_number", pymongo.ASCENDING)], unique=True)


def insert_user_request(user_dict: dict) -> str:
    """
    Add user
    """
    try:
        phone_number = user_dict.get("phone_number", None)
        email = user_dict.get("email", None)

        filter_dict = {}
        if phone_number:
            filter_dict = {'phone_number': phone_number}
        if email:
            filter_dict = {'email': email}
        response_data = filter_data(collection_name='users', filter_dict=filter_dict)
        if response_data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Phone Number or Email already exist")

        res_data = insert_item(collection_name='users', item_data=user_dict)
        print("---res_data---", res_data)
        # else:
        #     log.error(f"User not found after insertion")
        #     raise HTTPException(status_code=409, detail="User not found after insertion")
    except Exception as e:
        log.error(f"Error while inserting a user into the database: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


def update_user_request(user_id: str, user_dict: dict) -> Any:
    """
    Update user
    """
    try:
        response_data = update_item(collection_name='users', item_id=user_id, item_data=user_dict)
        return response_data
    except Exception as e:
        log.error(f"Error while inserting a user into the database: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


def get_user_by_id(user_id: str) -> Any:
    """
    Update user
    """
    try:
        response_data = get_item(collection_name='users', item_id=user_id)
        return response_data
    except Exception as e:
        log.error(f"Error while getting a user from the database: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


def get_users_list() -> Any:
    """
    Update user
    """
    try:
        response_data = get_item_list(collection_name='users')
        return response_data
    except Exception as e:
        log.error(f"Error while getting a user from the database: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


