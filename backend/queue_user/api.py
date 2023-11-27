from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import Body, HTTPException
from fastapi.routing import APIRouter
from typing import Any

from ..utils import success_response
from .schema import RegisterQueueUser
from ..queries import insert_item, prepare_item_list
from .helpers import get_queue_using_service

router = APIRouter()
queue_user_collection = 'queue_user'


@router.post("/v1/queue_user", response_description="Add new queue user")
def create_queue_user(employee: RegisterQueueUser = Body(...)) -> Any:
    """
    Register Queue user
    """
    data_dict = jsonable_encoder(employee)
    queue_id = get_queue_using_service(data_dict)
    data_dict['queue_id'] = queue_id
    del data_dict['employee_id']
    del data_dict['service_id']
    data_inserted = insert_item(queue_user_collection, data_dict)
    response_data = success_response(data={'employee_id': str(data_inserted)}, message="Successfully inserted data")
    return JSONResponse(content=response_data, status_code=201)


@router.post("/v1/next_user", response_description="Add new queue user")
def create_queue_user(employee: RegisterQueueUser = Body(...)) -> Any:
    """
    Register Queue user
    """
    data_dict = jsonable_encoder(employee)
    queue_id = get_queue_using_service(data_dict)
    data_dict['queue_id'] = queue_id
    del data_dict['employee_id']
    del data_dict['service_id']
    data_inserted = insert_item(queue_user_collection, data_dict)
    response_data = success_response(data={'employee_id': str(data_inserted)}, message="Successfully inserted data")
    return JSONResponse(content=response_data, status_code=201)


