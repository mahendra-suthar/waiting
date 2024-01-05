from bson import ObjectId
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from typing import Any

from ..utils import success_response
from ..queries import prepare_item_list
from ..websocket import waiting_list_manager
from config.database import client_db

router = APIRouter()
queue_user_collection = 'queue_user'
queue_collection = 'queue'


@router.delete("/v1/blank_queue/{queue_id}", response_description="Remove queue user")
def make_blank_queue(queue_id: str) -> Any:
    """
    Register Queue user
    """
    queue_user_list = prepare_item_list({
        'collection_name': 'queue_user',
        'schema': ['_id', 'queue_id'],
        'filters': {'is_deleted': False, 'queue_id': queue_id}
    })
    data_list = queue_user_list.get('data', [])

    for data in data_list:
        # Example data with '_id' field
        print("------data----------", data)
        data = {"_id": ObjectId(data['_id'])}

        # Get the collection
        queue_user_collection = client_db['queue_user']

        # Use delete_one method to delete a document
        queue_user_collection.delete_one({"_id": data["_id"]})

    waiting_list = waiting_list_manager.get_waiting_list(queue_id)
    print("------waiting_list--------", waiting_list)
    if waiting_list:
        waiting_list_manager.clear_queue(queue_id)

    response_data = success_response(message="Successfully cleared queue")
    return JSONResponse(content=response_data, status_code=201)
