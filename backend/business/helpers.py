from fastapi import HTTPException, status
from bson import ObjectId
from typing import Any

from config.database import client_db
from ..queries import insert_item, update_item, get_item, get_item_list, filter_data, prepare_item_list, generate_mongo_query
from .schema import BusinessData
from ..utils import success_response


collection_name = 'business'
business_collection = client_db[collection_name]
category_collection = 'category'
employee_collection = 'employee'
queue_collection = 'queue'
user_collection = 'users'


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

    response_data = update_item(collection_name='business', item_id=business_id, item_data=business_dict)
    return response_data


def prepare_category_wise_business_list():
    pipeline = [
        {
            "$group": {
                "_id": "$category_id",
                "businesses": {"$push": "$$ROOT"}
            }
        }
    ]
    grouped_businesses = business_collection.aggregate(pipeline)
    query, projections = generate_mongo_query(filter_conditions={'is_deleted': False}, projection_fields=["_id", "name"])
    category_list = client_db[category_collection].find(query, projections)
    category_dict = {str(category['_id']): category['name'] for category in category_list}

    business_groups = [
        {
            "category_id": str(group["_id"]),
            "category_name": category_dict.get(group['_id']),
            "businesses": [{**business, '_id': str(business['_id'])} for business in group["businesses"]]}
        for group in grouped_businesses if group
    ]
    return success_response(data=business_groups, message="Data get successfully")


def prepare_business_details_with_employee_queue(data_dict):
    business_id = data_dict.get('business_id')
    category_details = {}
    business_details = {}
    if business_id:
        business_response = get_item(
            collection_name=collection_name,
            item_id=ObjectId(business_id),
            filters={'_id': ObjectId(business_id)},
            columns=['name', 'category_id', 'phone', 'email', 'country_code', "address_id"]
        )

        business_details = business_response.get("data")
        category_id = business_details.get("category_id")
        if category_id:
            category_response = get_item(category_collection, category_id, None, columns=['name'])
            category_details = category_response.get('data', {})

        employee_list_dict = {
            'collection_name': employee_collection,
            'schema': ['email', 'phone_number', 'country_code', 'employee_number'],
            'filters': {'merchant_id': business_id}
        }
        employees_response = prepare_item_list(employee_list_dict)
        employee_list = employees_response.get('data', [])

        queue_list_dict = {
            'collection_name': queue_collection,
            'schema': ['employee_id', 'limit', 'status', 'current_length'],
            'filters': {'merchant_id': business_id}
        }
        queue_response = prepare_item_list(queue_list_dict)
        queue_list = queue_response.get('data', [])

        user_list_dict = {
            'collection_name': user_collection,
            'schema': ['employee_id', 'full_name'],
            'filters': {'employee_id': {'$ne': None}}
        }
        user_response = prepare_item_list(user_list_dict)
        user_list = user_response.get('data', [])
        user_dict = {user['employee_id']: {**user} for user in user_list if user and user.get('employee_id')}

        queue_dict = {queue['employee_id']: {**queue} for queue in queue_list if queue.get('employee_id')}
        employee_list = [{
            **employee,
            'queue': queue_dict.get(employee['_id'], {}),
            'user': user_dict.get(employee['_id'], {})
        } for employee in employee_list if employee and queue_dict.get(employee["_id"])]

        business_details = {
            **business_details,
            'category_name': category_details.get("name"),
            "employees": employee_list
        }
    return success_response(data=business_details, message='Data get successfully')


