from fastapi.responses import JSONResponse
from fastapi import Body, HTTPException, Depends
from fastapi.routing import APIRouter
from typing import Any
from fastapi.encoders import jsonable_encoder

from ..utils import success_response, prepare_dropdown_data
from .schema import RegisterLeaveRequest, LeaveRequestData, LeaveRequestActions
from ..queries import insert_item, prepare_item_list, update_item, get_item_list
from ..constants import LEAVE_REJECTED
from ..auth.helpers import JWTBearer

router = APIRouter()
leave_collection = 'leave'
user_collection = 'users'
employee_collection = 'employee'


@router.post("/v1/leave_request", response_description="Leave Request")
def create_leave_request(leave_request: RegisterLeaveRequest = Body(...),
                         current_user: str = Depends(JWTBearer())) -> Any:
    """
    Register Leave Request API
    """
    inserted_id = insert_item(leave_collection, leave_request, current_user)
    response_data = success_response(data={'item_id': str(inserted_id)}, message="Successfully inserted data")
    return JSONResponse(content=response_data, status_code=201)


@router.get("/v1/leave_request", response_description="Get Leave Request List", dependencies=[Depends(JWTBearer())])
def get_leave_request_list(
        page_number: int = 1,
        page_size: int = 10,
        search_string: str = None,
        status: int = None
) -> Any:
    """
    Get Leave Request List API
    """
    data_dict = {
        'collection_name': leave_collection,
        'schema': LeaveRequestData,
        'page_number': page_number,
        'page_size': page_size,
        'search_string': search_string
    }
    if status:
        data_dict['filters'] = {'status': status}

    response_data = prepare_item_list(data_dict)
    data = response_data.get("data")
    emp_data = get_item_list(collection_name=employee_collection,
                             columns=['user_id', 'email', 'country_code', 'phone_number'])

    emp_data_list = emp_data.get('data', [])
    emp_dict = {str(emp['_id']): {**emp} for emp in emp_data_list if emp}

    user_data = get_item_list(collection_name=user_collection, columns=['full_name'])
    user_data_list = user_data.get('data', [])
    user_dict = {str(user['_id']): user['full_name'] for user in user_data_list if user}

    for item in data:
        item['emp'] = emp_dict.get(str(item['employee_id']), {})
        item['emp']['full_name'] = user_dict.get(item.get('emp', {}).get('user_id', None), None)

    status_code = response_data.get("status")
    return JSONResponse(content=response_data, status_code=status_code)


@router.get("/v1/leave_request/{business_id}",
            response_description="Get Business leave request",
            dependencies=[Depends(JWTBearer())])
def get_business_leave_request_list(
        page_number: int = 1,
        page_size: int = 10,
        search_string: str = None,
        status: int = None
) -> Any:
    """
    Get Leave Request List API
    """
    data_dict = {
        'collection_name': leave_collection,
        'schema': LeaveRequestData,
        'page_number': page_number,
        'page_size': page_size,
        'search_string': search_string
    }
    if status:
        data_dict['filters'] = {'status': status}

    response_data = prepare_item_list(data_dict)
    data = response_data.get("data")
    emp_data = get_item_list(collection_name=employee_collection,
                             columns=['user_id', 'email', 'country_code', 'phone_number'])

    emp_data_list = emp_data.get('data', [])
    emp_dict = {str(emp['_id']): {**emp} for emp in emp_data_list if emp}

    user_data = get_item_list(collection_name=user_collection, columns=['full_name'])
    user_data_list = user_data.get('data', [])
    user_dict = {str(user['_id']): user['full_name'] for user in user_data_list if user}

    for item in data:
        item['emp'] = emp_dict.get(str(item['employee_id']), {})
        item['emp']['full_name'] = user_dict.get(item.get('emp', {}).get('user_id', None), None)

    status_code = response_data.get("status")
    return JSONResponse(content=response_data, status_code=status_code)


@router.put("/v1/leave_actions/{leave_id}", response_description="Approve or Reject leave")
def approve_or_reject_leave_request(
        leave_id: str,
        updated_data: LeaveRequestActions = Body(...),
        current_user: str = Depends(JWTBearer())
) -> Any:
    """
    Actions on Leave Request List API
    """
    updated_dict = jsonable_encoder(updated_data)
    response_data = update_item(leave_collection, item_id=leave_id, item_data=updated_dict, updated_by=current_user)
    status_code = response_data.get("status")
    return JSONResponse(content=response_data, status_code=status_code)
