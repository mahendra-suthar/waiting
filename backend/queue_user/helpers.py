from logs import logger as log
from fastapi import HTTPException

from .schema import QueueUserData
from ..queries import prepare_item_list, filter_data, get_item, update_item, update_items
from ..constants import QUEUE_USER_REGISTERED, QUEUE_USER_COMPLETED, QUEUE_USER_IN_PROGRESS
from ..websocket import waiting_list_manager

queue_user_collection = 'queue_user'
queue_collection = 'queue'


def jinja_variables_for_queue_user():
    data_dict = {
        'collection_name': queue_user_collection,
        'schema': QueueUserData
    }
    columns = list(QueueUserData.__annotations__.keys())
    data = prepare_item_list(data_dict)
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


def update_queue(user_id, queue_id):
    if user_id:
        data_dict = {
            'collection_name': queue_user_collection,
            'filters': {'is_deleted': False, 'queue_id': queue_id, 'status': int(QUEUE_USER_REGISTERED)}
        }
        current_length = len(prepare_item_list(data_dict).get('data'))
        data_dict = {'current_length': current_length}
        if current_length <= 1:
            data_dict['current_user'] = str(user_id)
        update_item(queue_collection, queue_id, data_dict)
        waiting_list_manager.load_waiting_list_from_volume()
        waiting_list_manager.add_customer(queue_id, str(user_id))
        print("---------waliting list---------", waiting_list_manager.get_waiting_list(queue_id))


def prepare_next_user(queue_id):
    waiting_list = waiting_list_manager.get_waiting_list(queue_id)
    current_user = waiting_list[0] if len(waiting_list) > 0 else None
    next_user = waiting_list[1] if len(waiting_list) > 1 else None
    print("=====current_user==1===", current_user)
    data_dict = {'status': QUEUE_USER_COMPLETED}
    match_dict = {'user_id': current_user, 'queue_id': queue_id}
    print("=====data_dict==1===", data_dict)
    return_data = update_items(queue_user_collection, match_dict, data_dict)
    if return_data:
        print("=====message=current_user=====", return_data['message'])
        waiting_list_manager.remove_customer(current_user)

    print("=====next_user==1===", next_user)
    match_dict = {'user_id': next_user, 'queue_id': queue_id}
    data_dict = {'status': QUEUE_USER_IN_PROGRESS}
    print("======data_dict=2===", data_dict)
    return_data = update_items(queue_user_collection, match_dict, data_dict)
    if return_data:
        print("=====message=next_user=====", return_data['message'])
        waiting_list_manager.add_customer(next_user)

    return {'next_user': next_user}


