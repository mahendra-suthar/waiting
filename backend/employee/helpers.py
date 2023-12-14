from .schema import EmployeeData
from config.database import client_db
from ..queries import prepare_item_list
from ..constants import queue_user_status_choices
from ..websocket import waiting_list_manager

employee_collection = 'employee'
queue_user_collection = 'queue_user'
user_collection = 'users'


def jinja_variables_for_employees():
    data_dict = {
        'collection_name': employee_collection,
        'schema': EmployeeData
    }
    columns = list(EmployeeData.__annotations__.keys())

    data = prepare_item_list(data_dict)
    table_name = employee_collection
    name = 'Employee'
    return columns, data, name, table_name


# async def insert_employee_request(employee_dict: dict) -> str:
#     """
#     Add user
#     """
#     res_data = insert_item(collection_name='users', item_data=employee_dict)
#     return res_data


def prepare_employee_queue_history(employee_dict: dict):
    final_list = []
    queue_id = employee_dict.get('queue_id')
    user_list_dict = {
        'collection_name': user_collection,
        'schema': ['full_name', 'country_code', 'phone_number', 'email', 'date_of_birth', 'gender']
    }
    user_response = prepare_item_list(user_list_dict)
    user_list = user_response.get('data', [])
    user_dict = {user['_id']: {**user} for user in user_list if user}

    if queue_id:
        pipeline = [
            {
                "$match": {
                    "is_deleted": False,
                    "queue_id": queue_id
                }
            },
            {
                "$group": {
                    "_id": "$status",
                    "queue_user": {"$push": "$$ROOT"}
                }
            }
        ]
        grouped_queue_user = client_db[queue_user_collection].aggregate(pipeline)
        queue_user_status_dict = dict(queue_user_status_choices)
        final_list = []
        for group in grouped_queue_user:
            current_length = 0
            data_dict = dict()
            data_dict['status'] = {'value': group['_id'], 'label': queue_user_status_dict[group['_id']]}
            data_dict['queue_user_details'] = []
            for queue_user in group['queue_user']:
                queue_id = queue_user['queue_id']
                waiting_list = waiting_list_manager.get_waiting_list(queue_id)
                queue_user['current_length'] = current_length
                user_id = queue_user.get('user_id')
                queue_users_dict = {
                    'id': str(queue_user['_id']),
                    'user_details': user_dict.get(user_id),
                    'current_length': len(waiting_list),
                }
                if waiting_list and user_id in waiting_list:
                    queue_users_dict['place_in_queue'] = waiting_list.index(queue_user.get('user_id'))

                data_dict['queue_user_details'].append(queue_users_dict)
            final_list.append(data_dict)

    return {'data': final_list}


def prepare_employee_queue_history_as_per_status(employee_dict: dict):
    data_dict = {}
    queue_id = employee_dict.get('queue_id')
    status = employee_dict.get('status')
    user_list_dict = {
        'collection_name': user_collection,
        'schema': ['full_name', 'country_code', 'phone_number', 'email', 'date_of_birth', 'gender']
    }
    user_response = prepare_item_list(user_list_dict)
    user_list = user_response.get('data', [])
    user_dict = {user['_id']: {**user} for user in user_list if user}

    if queue_id:
        queue_list_dict = {
            'collection_name': queue_user_collection,
            'schema': ['user_id', 'queue_id', 'status', 'enqueue_time', 'priority'],
            'filters': {'queue_id': queue_id, 'status': status}
        }
        queue_user_response = prepare_item_list(queue_list_dict)
        queue_user_list = queue_user_response.get('data', [])
        queue_user_status_dict = dict(queue_user_status_choices)
        current_length = 0
        data_dict = dict()
        data_dict['status'] = {'value': status, 'label': queue_user_status_dict[status]}
        data_dict['queue_user_details'] = []
        for queue_user in queue_user_list:
            queue_id = queue_user['queue_id']
            waiting_list = waiting_list_manager.get_waiting_list(queue_id)
            queue_user['current_length'] = current_length
            user_id = queue_user.get('user_id')
            queue_users_dict = {
                'id': str(queue_user['_id']),
                'user_details': user_dict.get(user_id),
                'current_length': len(waiting_list),
            }
            if waiting_list and user_id in waiting_list:
                queue_users_dict['place_in_queue'] = waiting_list.index(queue_user.get('user_id'))

            data_dict['queue_user_details'].append(queue_users_dict)

    return {'data': data_dict}