from .schema import QueueData
from ..queries import prepare_item_list, get_item_list

queue_collection = 'queue'
users_collection = 'users'


def jinja_variables_for_queue():
    data_dict = {
        'collection_name': queue_collection,
        'schema': QueueData
    }
    columns = list(QueueData.__annotations__.keys())
    data = prepare_item_list(data_dict)

    user_data = get_item_list(collection_name=users_collection, columns=['full_name'])
    user_data_list = user_data.get('data', [])
    user_data_dict = {user['_id']: user['full_name'] for user in user_data_list if user}
    for item in data['data']:
        item['current_user'] = user_data_dict.get(item['current_user'])

    table_name = queue_collection
    name = 'Queue'
    return columns, data, name, table_name
