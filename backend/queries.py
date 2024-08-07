from bson import ObjectId
from fastapi import status
from typing import Any
from fastapi import HTTPException
from pymongo import UpdateOne
from fastapi.encoders import jsonable_encoder

from logs import logger as log
from config.database import client_db
from .utils import success_response, error_response, get_current_timestamp_utc


def filter_data(
    collection_name: str = None,
    filter_dict: dict = None
) -> Any:
    # try:
    collection = client_db[collection_name]
    if not filter_dict:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="filter dict not found")

    if not filter_dict.get('is_deleted'):
        filter_dict['is_deleted'] = False

    result = collection.find_one(filter_dict)
    if result:
        return True
    else:
        return False
    # except Exception as error:
    #     log.error(f"Error while getting a {collection_name} from the database: {str(error)}")
    #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


# def filter_data_dict(
#     collection_name: str = None,
#     filter_dict: dict = None
# ) -> Any:
#     # try:
#     collection = client_db[collection_name]
#     if not filter_dict:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="filter dict not found")
#
#     if not filter_dict.get('is_deleted'):
#         filter_dict['is_deleted'] = False
#
#     result = collection.find_one(filter_dict)
#     return result


def insert_item(
    collection_name: str = None,
    item_data: any = None,
    created_by: any = None
) -> Any:
    collection = client_db[collection_name]
    if not item_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item data not found")

    if not isinstance(item_data, dict):
        item_data = jsonable_encoder(item_data)

    item_data['created_at'] = get_current_timestamp_utc()
    item_data['created_by'] = created_by
    item_data['updated_by'] = None
    item_data['updated_at'] = get_current_timestamp_utc()
    item_data['is_deleted'] = False
    try:
        result = collection.insert_one(item_data)
        inserted_id = result.inserted_id
    except Exception as error:
        inserted_id = None
        log.error(f"Error while inserting data into {collection_name}: {str(error)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error while inserting data into {collection_name}"
        )

    return inserted_id


def get_item(
    collection_name: str = None,
    item_id: str = None,
    filters: dict = None,
    columns: list = None
) -> Any:
    try:
        if not columns:
            columns = []

        collection = client_db[collection_name]
        if not item_id:
            return error_response(status=status.HTTP_400_BAD_REQUEST, error="Item id not found")

        filter_dict = {'is_deleted': False, '_id': ObjectId(item_id)}
        if filters:
            filter_dict.update(filters)

        query, projections = generate_mongo_query(filter_conditions=filter_dict, projection_fields=columns)
        result = collection.find_one(query, {**projections})
        if result:
            result['_id'] = str(result['_id'])
            return success_response(data=result, status=status.HTTP_200_OK, message="Data get successfully")
        else:
            return error_response(status=status.HTTP_400_BAD_REQUEST, error="Data not found")
    except Exception as error:
        log.error(f"Error while getting a {collection_name} from the database: {str(error)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


def get_item_list(
    collection_name: str = None,
    columns: list = None
) -> Any:
    if not columns:
        columns = []
    collection = client_db[collection_name]
    columns_dict = {column: 1 for column in columns}

    result = collection.find({"is_deleted": False}, columns_dict)
    if result:
        documents = [{**doc, '_id': str(doc['_id'])} for doc in result]
        return success_response(data=documents, status=status.HTTP_200_OK, message="Data get successfully")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Data not found")


def prepare_item_list(data_dict: dict) -> Any:
    # Extract data from data_dict
    collection_name = data_dict.get('collection_name', None)
    schema = data_dict.get('schema', None)
    page_number = data_dict.get('page_number', 0)
    page_size = data_dict.get('page_size', 10)
    search_string = data_dict.get('search_string', None)
    foreign_keys = data_dict.get("foreign_keys", {})
    filters = data_dict.get('filters')

    collection = client_db[collection_name]

    # columns to show
    if not isinstance(schema, list):
        schema = list(schema.__annotations__.keys()) if schema else []

    # preparing query using common function
    filter_conditions = {'is_deleted': False}
    if filters:
        filter_conditions.update(**filters)
    filter_query, projection = generate_mongo_query(filter_conditions, projection_fields=schema)

    # Foreign key data
    # if foreign_keys:
    #     sub_collection = client_db[foreign_keys['collection']]
    #     columns = foreign_keys['columns']
    #     filter_query, projection = generate_mongo_query(filter_conditions, projection_fields=columns)
    #     result = sub_collection.find(filter_conditions, projection)
    #     sub_documents = {{str(doc['_id']): doc} for doc in result}

    print("-------filter_query-------", filter_query)

    # preparing pagination data
    # if page_number < 1 or page_size < 1:
    #     raise HTTPException(status_code=400, detail="Invalid page or page_size")
    if page_number and page_size:
        skip = (page_number - 1) * page_size
        limit = page_size
        result = collection.find(filter_query, {**projection}).skip(skip).limit(limit)
    else:
        result = collection.find(filter_query, {**projection})

    if result:
        documents = [{**doc, '_id': str(doc['_id'])} for doc in result]
        return success_response(data=documents, status=status.HTTP_200_OK, message="Data get successfully")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Data not found")


def update_item(
    collection_name: str = None,
    item_id: str = None,
    item_data: dict = None,
    updated_by: str = None
) -> dict:
    try:
        print("-------item_id, item_data------", item_id, item_data)
        collection = client_db[collection_name]
        if not item_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item id not found")
        if not item_data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Updated data not found")

        # query = generate_mongo_query({'is_deleted': False, 'name': item_data['name'], '_id': {'$ne': item_id}})
        # if collection.find_one(query):
        #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Category already exist")

        item_data['updated_at'] = get_current_timestamp_utc()
        item_data['updated_by'] = updated_by
        print("-------item_id, item_data------", item_id, item_data)
        result = collection.update_one(
            {"_id": ObjectId(item_id)},
            {"$set": item_data}
        )

        if result.modified_count == 1:
            return success_response(status=status.HTTP_200_OK, message="Successfully updated data")
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item not found")

    except Exception as error:
        log.error(f"Error while updating a {collection_name} into the database: {str(error)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


def update_items(
    collection_name: str = None,
    match_dict: dict = None,
    update_dict: dict = None,
    updated_by: str = None
) -> dict:
    try:
        collection = client_db[collection_name]
        if not match_dict:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="match dict not found")
        if not update_dict:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Update data not found")

        update_dict['updated_at'] = get_current_timestamp_utc()
        update_dict['updated_by'] = updated_by
        print("----match_dict, update_dict------", match_dict, update_dict)
        result = collection.update_one(
            match_dict,
            {"$set": update_dict}
        )

        if result.modified_count == 1:
            return success_response(status=status.HTTP_200_OK, message="Successfully updated data")
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item not found")

    except Exception as error:
        log.error(f"Error while updating a {collection_name} into the database: {str(error)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


def delete_item(collection_name: str, item_id: str) -> bool:
    try:
        collection = client_db[collection_name]
        result = collection.update_one(
            {"_id": ObjectId(item_id)},
            {"$set": {'is_deleted': True}}
        )
        if result.modified_count == 1:
            return success_response(status=status.HTTP_200_OK, message="Successfully deleted data")
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item not found")
    except Exception as error:
        log.error(f"Error while deleting a {collection_name} into the database: {str(error)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


def generate_mongo_query(filter_conditions=None, projection_fields=None):
    """
    Generate a MongoDB query.

    Args:
    - collection_name: The name of the MongoDB collection to query.
    - filter_conditions: A dictionary specifying the filter conditions (optional).
    - projection_fields: A list of fields to include or exclude from the result (optional).

    Returns:
    - query: The MongoDB query as a dictionary.
    """
    query = {}

    if filter_conditions:
        for field, condition in filter_conditions.items():
            if condition is None:
                continue
            if isinstance(condition, dict):
                query[field] = condition
            else:
                query[field] = {'$eq': condition}

    projection = {}
    if projection_fields:
        for field in projection_fields:
            projection[field] = 1

    return query, projection


def generate_mongo_update_query(filter_conditions, update_data):
    """
    Generate a MongoDB update query.

    Args:
    - collection_name: The name of the MongoDB collection to update.
    - filter_conditions: A dictionary specifying the filter conditions to identify documents to update.
    - update_data: A dictionary specifying the update operations to perform.

    Returns:
    - query: A list of MongoDB UpdateOne objects.
    """
    update_query = []

    if filter_conditions and update_data:
        update_query.append(UpdateOne(filter_conditions, {'$set': update_data}))

    return update_query
