from fastapi import HTTPException, Depends, Body
from bson import ObjectId
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from typing import Any

from ..utils import success_response, get_current_timestamp_utc, get_current_date_str
from ..queries import prepare_item_list, update_items, get_item, insert_item
from ..websocket import waiting_list_manager
from config.database import client_db
from ..constants import QUEUE_USER_IN_PROGRESS, QUEUE_RUNNING_STOP, QUEUE_RUNNING_START, QUEUE_USER_COMPLETED, \
    queue_user_status_choices
from .schema import RegisterQueue
from ..auth.helpers import JWTBearer

router = APIRouter()
queue_user_collection = 'queue_user'
queue_collection = 'queue'
employee_collection = 'employee'
user_collection = 'users'


@router.post("/v1/queue", response_description="Create Queue")
def create_queue(queue_data: RegisterQueue = Body(...), current_user: str = Depends(JWTBearer())) -> Any:
    """
    Register Queue Post API
    """
    inserted_id = insert_item(queue_collection, queue_data, current_user)
    response_data = success_response(data={'item_id': str(inserted_id)}, message="Successfully inserted data")
    return JSONResponse(content=response_data, status_code=201)


@router.get("/v1/start_queue/{queue_id}", response_description="Start queue", dependencies=[Depends(JWTBearer())])
def start_queue(queue_id: str) -> Any:
    """
    Start Queue
    """
    if not queue_id:
        raise HTTPException(status_code=400, detail="Queue Id not exist")

    date_str = get_current_date_str()
    waiting_list = waiting_list_manager.get_waiting_list(queue_id, date_str)
    first_user = waiting_list[0] if len(waiting_list) > 0 else None

    data_dict = get_item(queue_collection, item_id=queue_id, columns=['current_user'])['data']
    current_user = data_dict['current_user']

    # if not current_user:
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
    # else:
    #     response_data = success_response(message="Current user exist")
    return JSONResponse(content=response_data, status_code=201)


@router.get("/v1/stop_queue/{queue_id}", response_description="Stop queue", dependencies=[Depends(JWTBearer())])
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


@router.delete("/v1/blank_queue/{queue_id}",
               response_description="Remove queue user",
               dependencies=[Depends(JWTBearer())])
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
        data = {"_id": ObjectId(data['_id'])}
        queue_user_client = client_db['queue_user']

        # Use delete_one method to delete a document
        queue_user_client.delete_one({"_id": data["_id"]})

    date_str = get_current_date_str()
    waiting_list = waiting_list_manager.get_waiting_list(queue_id, date_str)
    if waiting_list:
        waiting_list_manager.clear_queue(queue_id)

    response_data = success_response(message="Successfully cleared queue")
    return JSONResponse(content=response_data, status_code=201)


@router.get("/v1/get_business_queue_details/{business_id}",
            response_description="Get Business Queue Details",
            dependencies=[Depends(JWTBearer())])
def get_business_queue_details(business_id: str):
    """
    Prepare Queue details as per business
    :param business_id:
    :return:
    """
    # date_str = get_current_date_str()
    user_details = {
        'collection_name': user_collection,
        'schema': ['full_name']
    }
    user_details_data = prepare_item_list(user_details).get('data', [])
    full_name_dict = {user.get('_id'): user.get('full_name') for user in user_details_data if user}

    employee_list_dict = {
        'collection_name': employee_collection,
        'schema': ['queue_id', 'user_id'],
        'filters': {'merchant_id': business_id}
    }
    employee_list_data = prepare_item_list(employee_list_dict).get('data', [])
    queue_staff_list = []
    other_staff_list = []

    for emp_dict in employee_list_data:
        queue_id = emp_dict.get('queue_id')
        employee_id = emp_dict.get('_id')
        full_name = full_name_dict.get(emp_dict.get('user_id'), "-")

        if queue_id and queue_id != "":
            pipeline = [
                {
                    "$match": {
                        "is_deleted": False,
                        "queue_id": queue_id
                    }
                },
                {
                    "$group": {
                        "_id": "$status",
                        "queue_user": {"$sum": 1}
                    }
                }
            ]
            grouped_queue_user = client_db[queue_user_collection].aggregate(pipeline)
            queue_user_status_dict = dict(queue_user_status_choices)
            status_count_dict = {
                queue_user_status_dict[queue['_id']]: queue.get('queue_user')
                for queue in grouped_queue_user
            }

            queue_staff_list.append(
                {
                    'queue_id': queue_id,
                    'employee_id': employee_id,
                    'full_name': full_name,
                    'status_count': status_count_dict
                }
            )
        else:
            other_staff_list.append({'employee_id': employee_id, 'full_name': full_name})

    final_dict = {
        'queue_staff_list': queue_staff_list,
        'other_staff_list': other_staff_list
    }

    response_data = success_response(data=final_dict, message="Successfully get data")
    return JSONResponse(content=response_data, status_code=201)
