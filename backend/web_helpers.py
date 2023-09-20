from .users.helpers import get_users_list


def jinja_variables_for_users():
    columns = ['_id', 'full_name', 'phone_number', 'email']
    data = get_users_list()
    table_name = "users"
    name = "Users"
    return columns, data, name, table_name
