from fastapi import HTTPException, status
from bson import ObjectId
from typing import Any

from config.database import client_db
from ..queries import insert_item, update_item, get_item, get_item_list, filter_data
from .schema import BusinessData
from ..queries import prepare_item_list


collection_name = 'business'
business_collection = client_db[collection_name]


def jinja_variables_for_business():
    data_dict = {
        'collection_name': collection_name,
        'schema': BusinessData
    }
    columns = list(BusinessData.__annotations__.keys())
    data = prepare_item_list(data_dict)
    table_name = collection_name
    name = 'Business'
    return columns, data, name, table_name


async def insert_business_request(business_dict: dict) -> str:
    """
    Add Business
    """

    is_email_exist = filter_data(collection_name='business', filter_dict={'email': business_dict.get("email")})
    if is_email_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exist")

    is_phone_exist = filter_data(
        collection_name='business',
        filter_dict={'phone_number': business_dict.get("phone_number")}
    )
    if is_phone_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Phone Number already exist")

    res_data = insert_item(collection_name='business', item_data=business_dict)
    return res_data


async def update_business_request(business_id: str, business_dict: dict) -> Any:
    """
    Update business
    """
    is_business_exist = filter_data(collection_name='business', filter_dict={'_id': ObjectId(business_id)})
    if not is_business_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Business not found with this Id")

    is_email_exist = filter_data(
        collection_name='business',
        filter_dict={'_id': {'$ne': ObjectId(business_id)}, 'email': business_dict.get("email")}
    )
    if is_email_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exist")

    is_phone_exist = filter_data(
        collection_name='business',
        filter_dict={'_id': {'$ne': ObjectId(business_id)}, 'phone': business_dict.get("phone_number")}
    )
    if is_phone_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Phone Number already exist")

    response_data = await update_item(collection_name='business', item_id=business_id, item_data=business_dict)
    return response_data



