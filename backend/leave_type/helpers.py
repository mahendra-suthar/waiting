from .schema import LeaveTypeData, LeaveBalanceData
from ..queries import prepare_item_list

leave_type_collection = 'leave_type'
leave_balance_collection = 'leave_balance'


def jinja_variables_for_leave_type():
    data_dict = {
        'collection_name': leave_type_collection,
        'schema': LeaveTypeData
    }
    columns = list(LeaveTypeData.__annotations__.keys())
    data = prepare_item_list(data_dict)

    table_name = leave_type_collection
    name = 'Leave Type'
    return columns, data, name, table_name


def jinja_variables_for_leave_balance():
    data_dict = {
        'collection_name': leave_balance_collection,
        'schema': LeaveBalanceData
    }
    columns = list(LeaveBalanceData.__annotations__.keys())
    data = prepare_item_list(data_dict)

    table_name = leave_balance_collection
    name = 'Leave Balance'
    return columns, data, name, table_name