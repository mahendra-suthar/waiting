from fastapi.responses import JSONResponse
from fastapi import Body, HTTPException
from fastapi.routing import APIRouter
from typing import Any
from fastapi.encoders import jsonable_encoder

from ..utils import success_response, prepare_dropdown_data
from .schema import RegisterLeaveRequest, LeaveRequestData, LeaveRequestActions
from ..queries import insert_item, prepare_item_list, update_item
from ..constants import LEAVE_REJECTED

router = APIRouter()
leave_collection = 'leave'


@router.post("/v1/leave_request", response_description="Leave Request")
def create_leave_request(leave_request: RegisterLeaveRequest = Body(...)) -> Any:
    """
    Register Leave Request API
    """
    inserted_id = insert_item(leave_collection, leave_request)
    response_data = success_response(data={'item_id': str(inserted_id)}, message="Successfully inserted data")
    return JSONResponse(content=response_data, status_code=201)


@router.get("/v1/leave_request", response_description="Get Leave Request List")
def get_service(
        page_number: int = 1,
        page_size: int = 10,
        search_string: str = None
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
    response_data = prepare_item_list(data_dict)
    status_code = response_data.get("status")
    return JSONResponse(content=response_data, status_code=status_code)


@router.put("/v1/leave_actions/{leave_id}", response_description="Approve or Reject leave")
def approve_or_reject_leave_request(
        leave_id: str,
        updated_data: LeaveRequestActions = Body(...),
) -> Any:
    """
    Actions on Leave Request List API
    """
    updated_dict = jsonable_encoder(updated_data)
    response_data = update_item(leave_collection, item_id=leave_id, item_data=updated_dict)
    status_code = response_data.get("status")
    return JSONResponse(content=response_data, status_code=status_code)
