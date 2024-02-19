from fastapi import HTTPException, status
from bson import ObjectId
from typing import Any

from config.database import client_db
from ..queries import insert_item, update_item, get_item, get_item_list, filter_data, prepare_item_list, generate_mongo_query
from .schema import BusinessData
from ..utils import success_response, generate_qr_code
from ..constants import MERCHANT, business_status_choices


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
    columns = list(BusinessData.__annotations__.keys()) + ['category']
    data = prepare_item_list(data_dict)

    category_data = get_item_list(collection_name=category_collection, columns=['name'])
    category_data_list = category_data.get('data', [])
    category_data_dict = {category['_id']: category['name'] for category in category_data_list if category}
    for item in data['data']:
        item['category'] = category_data_dict.get(item['category_id'])

    status_dict = dict(business_status_choices)
    for item in data['data']:
        item['status'] = status_dict.get(item['status'])

    columns.remove('category_id')
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

    owner_exist = filter_data(collection_name='users', filter_dict={'_id': ObjectId(business_dict.get("owner_id"))})
    if not owner_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Owner not found")

    # qr_file_path = generate_qr_code('http://ec2-35-154-41-121.ap-south-1.compute.amazonaws.com:8000/web/business')
    business_dict['qr_code'] = None
    inserted_id = insert_item(collection_name='business', item_data=business_dict)

    user_id = business_dict.get('owner_id')
    if inserted_id and user_id:
        qr_file_path = generate_qr_code(str(inserted_id))
        update_item(business_collection, str(inserted_id), {'qr_code': qr_file_path})

        update_item(user_collection, str(user_id), {'user_type': MERCHANT})
    return inserted_id


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
            "$match": {
                "is_deleted": False
            }
        },
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
    # category_dict = {str(category['_id']): category['name'] for category in category_list}
    category_business_list = {str(group['_id']): [{**business, '_id': str(business['_id'])} for business in group["businesses"]] for group in grouped_businesses}
    # business_groups = [
    #     {
    #         "category_id": str(group["category_id"]),
    #         "category_name": category_dict.get(group['category_id']),
    #         "businesses": [{**business, '_id': str(business['_id'])} for business in group["businesses"]]}
    #     for group in grouped_businesses if group
    # ]
    business_groups = [
        {
            "category_id": str(category['_id']),
            "category_name": category['name'],
            "businesses": category_business_list.get(str(category['_id']), [])}
        for category in category_list if category
    ]
    return success_response(data=business_groups, message="Data get successfully")


def prepare_business_details_with_employee_queue(data_dict):
    business_id = data_dict.get('business_id')
    category_details = {}
    business_details = {}
    if business_id:
        business_response = get_item(
            collection_name=collection_name,
            item_id=business_id,
            filters={'_id': ObjectId(business_id)},
            columns=['name', 'category_id', 'phone', 'email', 'country_code', "address_id", 'about_business', 'phone_number']
        )
        business_details = business_response.get("data", {})
        category_id = business_details.get("category_id")
        if category_id:
            category_response = get_item(category_collection, category_id, None, columns=['name'])
            category_details = category_response.get('data', {})

        employee_list_dict = {
            'collection_name': employee_collection,
            'schema': ['email', 'phone_number', 'country_code', 'employee_number', 'user_id', 'queue_id'],
            'filters': {'merchant_id': business_id}
        }
        employees_response = prepare_item_list(employee_list_dict)
        employee_list = employees_response.get('data', [])

        queue_list_dict = {
            'collection_name': queue_collection,
            'schema': ['name', 'limit', 'status', 'current_length', 'current_user']
        }
        queue_response = prepare_item_list(queue_list_dict)
        queue_list = queue_response.get('data', [])

        user_list_dict = {
            'collection_name': user_collection,
            'schema': ['employee_id', 'full_name']
        }
        user_response = prepare_item_list(user_list_dict)
        user_list = user_response.get('data', [])
        user_dict = {user['_id']: {**user} for user in user_list if user}
        queue_dict = {queue['_id']: {**queue} for queue in queue_list if queue}

        employee_list = [{
            **employee,
            'queue': queue_dict.get(employee['queue_id'], {}),
            'employee_details': user_dict.get(employee.get('user_id'), {})
        } for employee in employee_list if employee]

        category_name = category_details.get("name") if category_details else None
        business_details = {
            **business_details,
            'category_name': category_name,
            "employees": employee_list
        }
    return success_response(data=business_details, message='Data get successfully')


