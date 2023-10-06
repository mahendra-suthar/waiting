from .schema import EmployeeData
from config.database import client_db
from ..queries import prepare_item_list

employee_collection = 'employee'


def jinja_variables_for_employees():
    data_dict = {
        'collection_name': employee_collection,
        'schema': EmployeeData
    }
    columns = list(EmployeeData.__annotations__.keys())

    data = prepare_item_list(data_dict)
    table_name = employee_collection
    name = 'Employee'
    return columns, data, name, table_name


# async def insert_employee_request(employee_dict: dict) -> str:
#     """
#     Add user
#     """
#     res_data = insert_item(collection_name='users', item_data=employee_dict)
#     return res_data
