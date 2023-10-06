from .schema import CategoryData, ParentCategory
from ..queries import prepare_item_list

category_collection = 'category'


def jinja_variables_for_category():
    data_dict = {
        'collection_name': category_collection,
        'schema': CategoryData,
    }
    columns = list(CategoryData.__annotations__.keys())
    data = prepare_item_list(data_dict)
    table_name = category_collection
    name = 'Category'
    return columns, data, name, table_name
