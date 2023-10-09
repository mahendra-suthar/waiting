from .schema import BusinessScheduleData
from ..queries import prepare_item_list

business_schedule_collection = 'business_schedule'


def jinja_variables_for_business_schedule():
    data_dict = {
        'collection_name': business_schedule_collection,
        'schema': BusinessScheduleData,
    }
    columns = list(BusinessScheduleData.__annotations__.keys())
    data = prepare_item_list(data_dict)
    table_name = business_schedule_collection
    name = 'Business Schedule'
    return columns, data, name, table_name
