from .schema import QueueUserData
from ..queries import prepare_item_list

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
