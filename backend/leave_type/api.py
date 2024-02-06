from fastapi.responses import JSONResponse
from fastapi import Body, HTTPException
from fastapi.routing import APIRouter
from typing import Any
from fastapi.encoders import jsonable_encoder

from ..utils import success_response, prepare_dropdown_data
from .schema import RegisterLeaveType, RegisterLeaveBalance, LeaveTypeData, LeaveBalanceData
from ..queries import insert_item, prepare_item_list, update_item
from ..constants import LEAVE_REJECTED

router = APIRouter()
leave_type_collection = 'leave_type'
leave_balance_collection = 'leave_balance'


@router.post("/v1/leave_type", response_description="Leave Type")
def create_leave_request(leave_type: RegisterLeaveType = Body(...)) -> Any:
    """
    Register Leave Type API
    """
    inserted_id = insert_item(leave_type_collection, leave_type)
    response_data = success_response(data={'item_id': str(inserted_id)}, message="Successfully inserted data")
    return JSONResponse(content=response_data, status_code=201)


@router.get("/v1/leave_type", response_description="Get Leave Type List")
def get_service(
        page_number: int = 1,
        page_size: int = 10,
        search_string: str = None
) -> Any:
    """
    Get Leave Request List API
    """
    data_dict = {
        'collection_name': leave_type_collection,
        'schema': LeaveTypeData,
        'page_number': page_number,
        'page_size': page_size,
        'search_string': search_string
    }
    response_data = prepare_item_list(data_dict)
    status_code = response_data.get("status")
    return JSONResponse(content=response_data, status_code=status_code)


# Leave Balance
@router.post("/v1/leave_balance", response_description="Leave Balance")
def create_leave_balance(leave_balance: RegisterLeaveBalance = Body(...)) -> Any:
    """
    Register Leave Balance API
    """
    inserted_id = insert_item(leave_balance_collection, leave_balance)
    response_data = success_response(data={'item_id': str(inserted_id)}, message="Successfully inserted data")
    return JSONResponse(content=response_data, status_code=201)


@router.get("/v1/leave_balance", response_description="Get Leave Balance List")
def get_leave_balance(
        page_number: int = 1,
        page_size: int = 10,
        search_string: str = None
) -> Any:
    """
    Get Leave Balance List API
    """
    data_dict = {
        'collection_name': leave_balance_collection,
        'schema': LeaveBalanceData,
        'page_number': page_number,
        'page_size': page_size,
        'search_string': search_string
    }
    response_data = prepare_item_list(data_dict)
    status_code = response_data.get("status")
    return JSONResponse(content=response_data, status_code=status_code)