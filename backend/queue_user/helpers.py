from bson import ObjectId
from .schema import QueueUserData
from ..queries import prepare_item_list, filter_data, get_item

queue_user_collection = 'queue_user'


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
            print("-------data_list----", data_list)
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
