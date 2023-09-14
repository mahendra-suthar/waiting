from bson import ObjectId
from fastapi import status
from typing import List, Any
from fastapi import HTTPException

from logs import logger as log
from config.database import client_db
from .utils import success_response, error_response


def filter_data(
    collection_name: str = None,
    filter_dict: dict = None
) -> Any:
    try:
        collection = client_db[collection_name]
        if not filter_dict:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="filter dict not found")

        result = collection.find_one(filter_dict)
        if result:
            return True
        else:
            return False
    except Exception as error:
        log.error(f"Error while getting a {collection_name} from the database: {str(error)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


def insert_item(
    collection_name: str = None,
    item_data: dict = None
) -> Any:
    try:
        collection = client_db[collection_name]
        if not item_data:
            HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item data not found")
        print("-----item_data---", item_data)
        result = collection.insert_one(item_data)
        print("-----result---", result)

    except Exception as error:
        log.error(f"Error while getting a {collection_name} from the database: {str(error)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


def get_item(
    collection_name: str = None,
    item_id: str = None,
) -> Any:
    try:
        collection = client_db[collection_name]
        if not item_id:
            return error_response(status=status.HTTP_400_BAD_REQUEST, error="Item id not found")

        result = collection.find_one({"_id": ObjectId(item_id), 'is_deleted': False})
        if result:
            result['_id'] = str(result['_id'])
            return success_response(data=result, status=status.HTTP_200_OK, message="Data get successfully")
        else:
            return error_response(status=status.HTTP_400_BAD_REQUEST, error="Data not found")
    except Exception as error:
        log.error(f"Error while getting a {collection_name} from the database: {str(error)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


def get_item_list(
    collection_name: str = None
) -> Any:
    try:
        collection = client_db[collection_name]

        # result = collection.find({"is_deleted": False})
        result = collection.find({})
        if result:
            documents = [{**doc, '_id': str(doc['_id'])} for doc in result]
            return success_response(data=documents, status=status.HTTP_200_OK, message="Data get successfully")
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Data not found")
    except Exception as error:
        log.error(f"Error while getting {collection_name} list from the database: {str(error)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


async def update_item(
    collection_name: str = None,
    item_id: str = None,
    item_data: dict = None
) -> dict:
    try:
        collection = client_db[collection_name]
        if not item_id:
            # return error_response(status=status.HTTP_400_BAD_REQUEST, error="Item id not found")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item id not found")
        if not item_data:
            # return error_response(status=status.HTTP_400_BAD_REQUEST, error="Updated data not found")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Updated data not found")

        result = collection.update_one(
            {"_id": ObjectId(item_id)},
            {"$set": item_data}
        )

        if result.modified_count == 1:
            return success_response(status=status.HTTP_200_OK, message="Successfully updated data")
        else:
            # return error_response(status=status.HTTP_400_BAD_REQUEST, error="Item not updated")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item not found")

    except Exception as error:
        log.error(f"Error while updating a {collection_name} into the database: {str(error)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
        # return error_response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, error=f"Internal server error")


# async def delete_item(db: AsyncIOMotorClient, collection_name: str, item_id: str) -> bool:
#     result = await db.get_database()[collection_name].delete_one({"_id": item_id})
#     return result.deleted_count == 1