from fastapi.responses import JSONResponse
from fastapi import Body, HTTPException, Depends
from fastapi.routing import APIRouter
from typing import Any
from fastapi.encoders import jsonable_encoder

from ..utils import success_response, prepare_dropdown_data
from .schema import RegisterAttendance, AttendanceData
from ..queries import insert_item, prepare_item_list, update_item, get_item_list
from ..constants import ATTENDANCE_CLOCK_IN, ATTENDANCE_CLOCK_OUT
from ..auth.helpers import JWTBearer

router = APIRouter()
attendance_collection = 'attendance'
employee_collection = 'employee'


@router.post("/v1/clock-in-out", response_description="Clock In Out")
def clock_in_out(attendance: RegisterAttendance = Body(...), current_user: str = Depends(JWTBearer())) -> Any:
    """
    Employee Clock In Out API
    """
    inserted_id = insert_item(attendance_collection, attendance, current_user)
    if inserted_id:
        update_item(
            employee_collection,
            str(attendance.employee_id),
            {'is_available': True if ATTENDANCE_CLOCK_IN == int(attendance.event_type) else False})
    response_data = success_response(data={'item_id': str(inserted_id)}, message="Successfully inserted data")
    return JSONResponse(content=response_data, status_code=201)