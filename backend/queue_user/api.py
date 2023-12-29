from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import Body, HTTPException, Depends
from fastapi.routing import APIRouter
from typing import Any

from ..utils import success_response
from .schema import RegisterQueueUser
from ..queries import insert_item, prepare_item_list, update_items, update_item, get_item
from .helpers import get_queue_using_service, update_queue, prepare_next_user, prepare_appointments_history
from ..constants import QUEUE_USER_REGISTERED, QUEUE_USER_COMPLETED, QUEUE_USER_IN_PROGRESS
from ..websocket import waiting_list_manager
from ..auth.helpers import JWTBearer

router = APIRouter()
queue_user_collection = 'queue_user'
queue_collection = 'queue'


@router.post("/v1/queue_user", response_description="Add new queue user")
def create_queue_user(queue_user: RegisterQueueUser = Body(...)) -> Any:
    """
    Register Queue user
    """
    data_dict = jsonable_encoder(queue_user)
    queue_id = get_queue_using_service(data_dict)
    data_dict['queue_id'] = str(queue_id)
    del data_dict['employee_id']
    del data_dict['service_id']
    data_inserted = insert_item(queue_user_collection, data_dict)
    if data_inserted:
        update_queue(data_dict['user_id'], str(queue_id))
    response_data = success_response(data={'employee_id': str(data_inserted)}, message="Successfully inserted data")
    return JSONResponse(content=response_data, status_code=201)


@router.post("/v1/next_user/{queue_id}", response_description="Next User")
def queue_next_user(queue_id: str) -> Any:
    """
    Next User
    """
    waiting_list = waiting_list_manager.get_waiting_list(queue_id)
    queue_data = get_item(
        collection_name=queue_collection,
        item_id=queue_id,
        columns=['_id', 'current_user']
    )
    current_user = queue_data.get('data', {}).get('current_user', None)
    if current_user:
        current_user = waiting_list[0] if len(waiting_list) > 0 else None
        next_user = waiting_list[1] if len(waiting_list) > 1 else None
        data_dict = {'status': QUEUE_USER_COMPLETED}
        match_dict = {'user_id': current_user, 'queue_id': queue_id}
        return_data = update_items(queue_user_collection, match_dict, data_dict)
        if return_data and queue_id:
            waiting_list_manager.remove_customer(queue_id)

        match_dict = {'user_id': next_user, 'queue_id': queue_id}
        data_dict = {'status': QUEUE_USER_IN_PROGRESS}
        return_data = update_items(queue_user_collection, match_dict, data_dict)
        if return_data and next_user and queue_id:
            data_dict = {
                'collection_name': queue_user_collection,
                'filters': {'is_deleted': False, 'queue_id': queue_id,
                            'status': {'$in': [int(QUEUE_USER_REGISTERED), int(QUEUE_USER_IN_PROGRESS)]}}
            }
            current_length = len(prepare_item_list(data_dict).get('data'))
            data_dict = {
                'current_length': current_length,
                'current_user': str(next_user)
            }
            update_item(queue_collection, queue_id, data_dict)
        print("======[waiting-list]=======", waiting_list_manager.get_waiting_list(queue_id))
        response_data = success_response(data=next_user, message="Successfully updated data")
    else:
        current_user = waiting_list[0] if len(waiting_list) > 0 else None
        match_dict = {'user_id': current_user, 'queue_id': queue_id}
        data_dict = {'status': QUEUE_USER_IN_PROGRESS}
        return_data = update_items(queue_user_collection, match_dict, data_dict)
        if return_data and current_user and queue_id:
            data_dict = {
                'collection_name': queue_user_collection,
                'filters': {'is_deleted': False, 'queue_id': queue_id,
                            'status': {'$in': [int(QUEUE_USER_REGISTERED), int(QUEUE_USER_IN_PROGRESS)]}}
            }
            current_length = len(prepare_item_list(data_dict).get('data'))
            data_dict = {
                'current_length': current_length,
                'current_user': str(current_user)
            }
            update_item(queue_collection, queue_id, data_dict)
        print("======[waiting-list]=======", waiting_list_manager.get_waiting_list(queue_id))
        response_data = success_response(data=current_user, message="Successfully updated data")
    return JSONResponse(content=response_data, status_code=201)


@router.post("/v1/current_user_appointments", response_description="Next User")
def current_users_appointments(current_user: str = Depends(JWTBearer())) -> Any:
    """
    Preparing current user's appointment history
    """
    data_dict = prepare_appointments_history(current_user)
    response_data = success_response(data=data_dict['data'], message="Successfully get data")
    return JSONResponse(content=response_data, status_code=201)






