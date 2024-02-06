from fastapi import HTTPException
from bson import ObjectId
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from typing import Any

from ..utils import success_response, get_current_timestamp_utc
from ..queries import prepare_item_list, update_items, get_item
from ..websocket import waiting_list_manager
from config.database import client_db
from ..constants import QUEUE_USER_IN_PROGRESS, QUEUE_RUNNING_STOP, QUEUE_RUNNING_START

router = APIRouter()
queue_user_collection = 'queue_user'
queue_collection = 'queue'


@router.get("/v1/start_queue/{queue_id}", response_description="Start queue")
def start_queue(queue_id: str) -> Any:
    """
    Start Queue
    """
    if not queue_id:
        raise HTTPException(status_code=400, detail="Queue Id not exist")

    waiting_list = waiting_list_manager.get_waiting_list(queue_id)
    first_user = waiting_list[0] if len(waiting_list) > 0 else None

    data_dict = get_item(queue_collection, item_id=queue_id, columns=['current_user'])['data']
    current_user = data_dict['current_user']

    if not current_user:
        match_dict = {'user_id': first_user, 'queue_id': queue_id}
        update_items(
            queue_user_collection,
            match_dict,
            {'status': QUEUE_USER_IN_PROGRESS, 'turn_time': get_current_timestamp_utc()}
        )
        update_items(
            queue_collection,
            {'_id': ObjectId(queue_id)},
            {'running_status': QUEUE_RUNNING_START}
        )
        response_data = success_response(message="Successfully Added current user and start")
    else:
        response_data = success_response(message="Current user exist")
    return JSONResponse(content=response_data, status_code=201)


@router.get("/v1/stop_queue/{queue_id}", response_description="Stop queue")
def start_queue(queue_id: str) -> Any:
    """
    Stop Queue
    """
    if not queue_id:
        raise HTTPException(status_code=400, detail="Queue Id not exist")

    update_items(
        queue_collection,
        {'_id': ObjectId(queue_id)},
        {'running_status': QUEUE_RUNNING_STOP}
    )
    response_data = success_response(message="Successfully Stopped")
    return JSONResponse(content=response_data, status_code=201)


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
