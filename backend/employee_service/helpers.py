from .schema import EmployeeServiceData
from ..queries import prepare_item_list

employee_service_collection = 'employee_service'


def jinja_variables_for_employee_service():
    data_dict = {
        'collection_name': employee_service_collection,
        'schema': EmployeeServiceData
    }
    columns = list(EmployeeServiceData.__annotations__.keys())

    data = prepare_item_list(data_dict)
    table_name = employee_service_collection
    name = 'Employee Service'
    return columns, data, name, table_name