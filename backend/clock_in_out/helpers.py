from .schema import AttendanceData
from ..queries import prepare_item_list

attendance_collection = 'attendance'


def jinja_variables_for_attendance():
    data_dict = {
        'collection_name': attendance_collection,
        'schema': AttendanceData
    }
    columns = list(AttendanceData.__annotations__.keys())
    data = prepare_item_list(data_dict)
    table_name = attendance_collection
    name = 'Attendance'
    return columns, data, name, table_name