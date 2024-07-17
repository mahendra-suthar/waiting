from .schema import ServiceData
from ..queries import prepare_item_list, get_item_list
from ..constants import service_status_choices

service_collection = 'service'
business_collection = 'business'


def jinja_variables_for_service():
    data_dict = {
        'collection_name': service_collection,
        'schema': ServiceData
    }
    columns = list(ServiceData.__annotations__.keys()) + ['business']
    data = prepare_item_list(data_dict)

    business_data = get_item_list(collection_name=business_collection, columns=['name'])
    business_data_list = business_data.get('data', [])
    business_dict = {business['_id']: business['name'] for business in business_data_list if business}
    service_status_dict = dict(service_status_choices)
    for item in data['data']:
        item['business'] = business_dict.get(item['merchant_id'])
        item['status'] = service_status_dict.get(item['status'])

    columns.remove('merchant_id')
    table_name = service_collection
    name = 'Service'
    return columns, data, name, table_name
