from .schema import LeaveRequestData
from ..queries import prepare_item_list

leave_collection = 'leave'
queue_collection = 'queue'
employee_collection = 'employee'
business_collection = 'business'
user_collection = 'users'
category_collection = 'category'


def jinja_variables_for_leave_request():
    data_dict = {
        'collection_name': leave_collection,
        'schema': LeaveRequestData
    }
    columns = list(LeaveRequestData.__annotations__.keys())
    data = prepare_item_list(data_dict)

    table_name = leave_collection
    name = 'Leave Request'
    return columns, data, name, table_name
