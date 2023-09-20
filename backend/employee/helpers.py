from fastapi import HTTPException, status

from config.database import client_db
from ..queries import insert_item, filter_data

user_collection = client_db['users']


async def insert_employee_request(employee_dict: dict) -> str:
    """
    Add user
    """
    collection_name = 'employee'
    email = employee_dict.get("email")
    phone_number = employee_dict.get("phone_number")

    is_email_exist = filter_data(collection_name, filter_dict={'email': email})
    if is_email_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exist")

    is_phone_exist = filter_data(
        collection_name,
        filter_dict={'phone_number': phone_number}
    )
    if is_phone_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Phone Number already exist")

    res_data = insert_item(collection_name='users', item_data=employee_dict)
    return res_data
