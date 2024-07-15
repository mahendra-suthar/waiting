from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import Body, HTTPException, Depends
from fastapi.routing import APIRouter
from typing import Any

from ..utils import success_response, get_current_timestamp_utc, get_current_date_str
from .schema import RegisterQueueUser
from ..queries import insert_item, prepare_item_list, update_items, update_item, get_item, filter_data
from .helpers import get_queue_using_service, update_queue, prepare_appointments_history
from ..constants import QUEUE_USER_REGISTERED, QUEUE_USER_COMPLETED, QUEUE_USER_IN_PROGRESS
from ..websocket import waiting_list_manager
from ..auth.helpers import JWTBearer

router = APIRouter()
queue_user_collection = 'queue_user'
queue_collection = 'queue'


@router.post("/v1/queue_user", response_description="Add new queue user")
def create_queue_user(queue_user: RegisterQueueUser = Body(...), current_user: str = Depends(JWTBearer())) -> Any:
    """
    Register Queue user
    """
    data_dict = jsonable_encoder(queue_user)
    queue_id = get_queue_using_service(data_dict)
    user_id = data_dict['user_id']
    data_dict['queue_id'] = str(queue_id)
    del data_dict['employee_id']
    del data_dict['service_id']
    print("q_user_obj", queue_id, user_id)
    if queue_id and user_id:
        q_user_obj = filter_data(
            collection_name='queue_user',
            filter_dict={
                'status': {'$in': [int(QUEUE_USER_REGISTERED), int(QUEUE_USER_IN_PROGRESS)]},
                'user_id': user_id, 'queue_id': queue_id
            }
        )
        print("q_user_obj", q_user_obj)
        if q_user_obj:
            raise HTTPException(status_code=400, detail="Data already exists")
    data_dict['enqueue_time'] = get_current_timestamp_utc()
    data_inserted = insert_item(queue_user_collection, data_dict, current_user)
    if data_inserted:
        date_str = get_current_date_str(data_dict['queue_date'])
        update_queue(data_dict['user_id'], str(queue_id), date_str)
    response_data = success_response(data={'employee_id': str(data_inserted)}, message="Successfully inserted data")
    return JSONResponse(content=response_data, status_code=201)


@router.post("/v1/next_user/{queue_id}", response_description="Next User")
def queue_next_user(queue_id: str, auth_user: str = Depends(JWTBearer())) -> Any:
    """
    Next User
    """
    if not queue_id:
        raise HTTPException(status_code=400, detail="Queue Id not exist")

    date_str = get_current_date_str()
    waiting_list = waiting_list_manager.get_waiting_list(queue_id, date_str)
    current_user = waiting_list[0] if len(waiting_list) > 0 else None
    next_user = waiting_list[1] if len(waiting_list) > 1 else None
    data_dict = {'status': QUEUE_USER_COMPLETED, "dequeue_time": get_current_timestamp_utc()}

    if current_user:
        match_dict = {'user_id': current_user, 'queue_id': queue_id}
        return_data = update_items(queue_user_collection, match_dict, data_dict)
        if return_data:
            date_str = get_current_date_str()
            waiting_list_manager.remove_customer(queue_id, date_str)
        if next_user:
            match_dict = {'user_id': next_user, 'queue_id': queue_id}
            data_dict = {'status': QUEUE_USER_IN_PROGRESS, 'turn_time': get_current_timestamp_utc()}
            return_data = update_items(queue_user_collection, match_dict, data_dict)
            if return_data:
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
            response_data = success_response(data=next_user, message="Successfully updated data")
        else:
            response_data = success_response(message="Next user not exist")
    else:
        response_data = success_response(message="Current user not exist")
    return JSONResponse(content=response_data, status_code=201)


@router.post("/v1/current_user_appointments", response_description="Next User")
def current_users_appointments(current_user: str = Depends(JWTBearer())) -> Any:
    """
    Preparing current user's appointment history
    """
    data_dict = prepare_appointments_history(current_user)
    response_data = success_response(data=data_dict['data'], message="Successfully get data")
    return JSONResponse(content=response_data, status_code=201)






