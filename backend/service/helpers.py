from .schema import ServiceData
from ..queries import prepare_item_list

service_collection = 'service'


def jinja_variables_for_service():
    data_dict = {
        'collection_name': service_collection,
        'schema': ServiceData
    }
    columns = list(ServiceData.__annotations__.keys())
    data = prepare_item_list(data_dict)
    table_name = service_collection
    name = 'Service'
    return columns, data, name, table_name
