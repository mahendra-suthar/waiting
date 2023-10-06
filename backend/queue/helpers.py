from .schema import QueueData
from ..queries import prepare_item_list

queue_collection = 'queue'


def jinja_variables_for_queue():
    data_dict = {
        'collection_name': queue_collection,
        'schema': QueueData
    }
    columns = list(QueueData.__annotations__.keys())
    data = prepare_item_list(data_dict)
    table_name = queue_collection
    name = 'Queue'
    return columns, data, name, table_name
