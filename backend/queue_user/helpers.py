from logs import logger as log
from fastapi import HTTPException, status
from bson import ObjectId
from datetime import datetime

from .schema import QueueUserData
from ..queries import prepare_item_list, get_item_list, get_item, update_item, update_items, filter_data
from ..constants import (QUEUE_USER_REGISTERED, QUEUE_USER_COMPLETED, QUEUE_USER_IN_PROGRESS, queue_user_status_choices,
                         QUEUE_USER_FAILED, QUEUE_USER_CANCELLED)
from ..websocket import waiting_list_manager
from ..utils import get_current_date_str

queue_user_collection = 'queue_user'
queue_collection = 'queue'
employee_collection = 'employee'
business_collection = 'business'
user_collection = 'users'
category_collection = 'category'


def jinja_variables_for_queue_user():
    data_dict = {
        'collection_name': queue_user_collection,
        'schema': QueueUserData
    }
    columns = list(QueueUserData.__annotations__.keys()) + ['queue', 'user']
    data = prepare_item_list(data_dict)

    user_data = get_item_list(collection_name=user_collection, columns=['full_name'])
    user_data_list = user_data.get('data', [])
    user_data_dict = {user['_id']: user['full_name'] for user in user_data_list if user}
    for item in data['data']:
        item['user'] = user_data_dict.get(item['user_id'])

    queue_data = get_item_list(collection_name=queue_collection, columns=['name'])
    queue_data_list = queue_data.get('data', [])
    queue_data_dict = {queue['_id']: queue['name'] for queue in queue_data_list if queue}
    for item in data['data']:
        item['queue'] = queue_data_dict.get(item['queue_id'])

    status_dict = dict(queue_user_status_choices)
    for item in data['data']:
        item['status'] = status_dict.get(item['status'])

    columns.remove('user_id')
    columns.remove('queue_id')
    table_name = queue_user_collection
    name = 'Queue User'
    return columns, data, name, table_name


def get_queue_using_service(data_dict):
    service_id = data_dict.get("service_id", None)
    employee_id = data_dict.get("employee_id", None)
    queue_id = data_dict.get("queue_id", None)

    if not queue_id:
        if service_id:
            filter_dict = {'is_deleted': False, "service_id": service_id}
            data_dict = {
                'collection_name': 'employee_service',
                'filters': filter_dict,
                'schema': ['employee_id']
            }
            data_list = prepare_item_list(data_dict)
            data = data_list.get('data', [])
            if len(data) > 0:
                employee_id = data[0].get("employee_id")

        if employee_id:
            queue = get_item(
                collection_name='employee',
                item_id=employee_id,
                columns=['_id']
            )
            queue_id = queue.get('data', {}).get('_id', None)

    return queue_id


def update_queue(user_id, queue_id, date_str=None):
    if user_id:
        data_dict = {
            'collection_name': queue_user_collection,
            'filters': {'is_deleted': False, 'queue_id': queue_id, 'status': int(QUEUE_USER_REGISTERED)}
        }
        current_length = len(prepare_item_list(data_dict).get('data'))
        data_dict = {'current_length': current_length}
        # if current_length <= 1:
        #     data_dict['current_user'] = str(user_id)
        update_item(queue_collection, queue_id, data_dict)
        waiting_list_manager.load_waiting_list_from_volume()
        waiting_list_manager.add_customer(queue_id, str(user_id), date_str)


def prepare_next_user(queue_id):
    date_str = get_current_date_str()
    waiting_list = waiting_list_manager.get_waiting_list(queue_id, date_str)
    current_user = waiting_list[0] if len(waiting_list) > 0 else None
    next_user = waiting_list[1] if len(waiting_list) > 1 else None
    print("=====current_user==1===", current_user)
    data_dict = {'status': QUEUE_USER_COMPLETED}
    match_dict = {'user_id': current_user, 'queue_id': queue_id}
    print("=====data_dict==1===", data_dict)
    return_data = update_items(queue_user_collection, match_dict, data_dict)
    if return_data:
        print("=====message=current_user=====", return_data['message'])
        date_str = get_current_date_str()
        waiting_list_manager.remove_customer(current_user, date_str)

    print("=====next_user==1===", next_user)
    match_dict = {'user_id': next_user, 'queue_id': queue_id}
    data_dict = {'status': QUEUE_USER_IN_PROGRESS}
    print("======data_dict=2===", data_dict)
    return_data = update_items(queue_user_collection, match_dict, data_dict)
    if return_data:
        print("=====message=next_user=====", return_data['message'])
        waiting_list_manager.add_customer(queue_id, next_user, date_str)

    return {'next_user': next_user}


def get_business_employee_by_queue():
    employee_list_dict = {
        'collection_name': employee_collection,
        'schema': ['email', 'phone_number', 'country_code', 'employee_number', 'user_id', 'queue_id', 'merchant_id'],
    }
    employees_response = prepare_item_list(employee_list_dict)
    employee_list = employees_response.get('data', [])

    user_list_dict = {
        'collection_name': user_collection,
        'schema': ['full_name']
    }
    user_response = prepare_item_list(user_list_dict)
    user_list = user_response.get('data', [])

    business_list_dict = {
        'collection_name': business_collection,
        'schema': ['name', 'email', 'phone_number', 'country_code', 'owner_id', 'category_id'],
    }
    business_response = prepare_item_list(business_list_dict)
    business_list = business_response.get('data', [])

    category_list_dict = {
        'collection_name': category_collection,
        'schema': ['name', 'description'],
    }
    category_response = prepare_item_list(category_list_dict)
    category_list = category_response.get('data', [])

    business_dict = {business['_id']: {**business} for business in business_list if business}
    user_dict = {user['_id']: {**user} for user in user_list if user}
    category_dict = {category['_id']: {**category} for category in category_list if category}

    queue_dict = {}
    for employee in employee_list:
        if employee and employee['queue_id']:
            print("-------business_dict--------", business_dict)
            print("-------employee['merchant_id']--------", employee['merchant_id'])
            business_details = business_dict[employee['merchant_id']]
            print("-------business_details--------", business_details)
            business_category = category_dict.get(business_details['category_id'])
            print("-------business_category--------", business_details['category_id'], category_dict, business_category)
            queue_dict[employee['queue_id']] = {
                'business_name': business_details['name'],
                'business_phone': f"{business_details['country_code']}-{business_details['phone_number']}",
                'business_email': business_details['email'],
                'business_category': business_category['name'],
                'employee_phone': f"{employee['country_code']}-{employee['phone_number']}",
                'employee_name': user_dict.get(employee['user_id'], None)
            }

    return queue_dict


def get_queue_user_filtered_data(user_id: str, status_list: list) -> list:
    business_dict = get_business_employee_by_queue()
    registered_filter = {
        'collection_name': queue_user_collection,
        'filters': {
            'is_deleted': False,
            "status": {'$in': status_list},
            'user_id': user_id
        },
        'schema': ['queue_id', 'user_id']
    }
    registered_list = prepare_item_list(registered_filter)
    registered_data = registered_list.get('data', [])
    for data in registered_data:
        data['queue_details'] = business_dict.get(data.get('queue_id', None), None)
        date_str = get_current_date_str()
        waiting_list = waiting_list_manager.get_waiting_list(data['queue_id'], date_str)
        data['place_in_queue'] = waiting_list.index(data['user_id']) if data['user_id'] in waiting_list else 0
    return registered_data


def prepare_appointments_history(user_id: str):
    progress_data = get_queue_user_filtered_data(
        user_id, [int(QUEUE_USER_IN_PROGRESS)]
    )
    registered_data = get_queue_user_filtered_data(
        user_id, [int(QUEUE_USER_REGISTERED)]
    )
    completed_data = get_queue_user_filtered_data(
        user_id, [int(QUEUE_USER_COMPLETED), int(QUEUE_USER_CANCELLED), int(QUEUE_USER_FAILED)]
    )
    final_list = [
        {
            'label': 'In-Progress',
            'queue_user_details': progress_data
        },
        {
            'label': 'Registered',
            'queue_user_details': registered_data
        },
        {
            'label': 'Completed',
            'queue_user_details': completed_data
        }
    ]
    return {'data': final_list}


def prepare_customer_report(user_id):
    data_dict = {
        'total_customers': 0,
        'new_customers': 0,
        'today_customers': {
            'total': 0,
            'status_breakdown': []
        }
    }

    if not user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User Id not found")

    queue_ids = []
    is_business = filter_data(business_collection, {'_id': ObjectId(user_id)})
    is_employee = filter_data(employee_collection, {'_id': ObjectId(user_id)})

    if is_business or is_employee:
        if is_business:
            employee_dict = {
                'collection_name': employee_collection,
                'filters': {'is_deleted': False, 'merchant_id': user_id},
                'schema': ['queue_id']
            }
        else:  # is_employee
            employee_dict = {
                'collection_name': employee_collection,
                'filters': {'is_deleted': False, '_id': ObjectId(user_id)},
                'schema': ['queue_id']
            }

        employee_list = prepare_item_list(employee_dict).get('data')
        queue_ids = [item['queue_id'] for item in employee_list]

    if queue_ids:
        queue_user_dict = {
            'collection_name': queue_user_collection,
            'filters': {'is_deleted': False, 'queue_id': {'$in': queue_ids}},
            'schema': ['_id', 'created_at', 'status']
        }
        queue_user_list = prepare_item_list(queue_user_dict).get('data')
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Queue not found")

    data_dict['total_customers'] = len(queue_user_list)
    today = datetime.now().date()
    status_dict = dict(queue_user_status_choices)

    status_breakdown = {}

    for user in queue_user_list:
        user_created_date = datetime.fromtimestamp(user['created_at']).date()

        if user_created_date == today:
            data_dict['new_customers'] += 1
            data_dict['today_customers']['total'] += 1

            status = user['status']
            if status in status_breakdown:
                status_breakdown[status]['count'] += 1
                status_breakdown[status]['customers'].append(user)
            else:
                status_breakdown[status] = {
                    'status': {'key': status, 'label': status_dict[status]},
                    'count': 1,
                    'customers': [user]
                }

    data_dict['today_customers']['status_breakdown'] = list(status_breakdown.values())
    return {'data': data_dict}
