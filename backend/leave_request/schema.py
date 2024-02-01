from typing import Optional
from pydantic import BaseModel, EmailStr, constr

from ..constants import QUEUE_USER_REGISTERED


class RegisterLeaveRequest(BaseModel):
    employee_id: str
    start_date_time: int
    end_date_time: int
    leave_type: Optional[int] = 1
    duration: int
    status: Optional[int] = 1
    requested_date: int
    approval_date: Optional[int] = None
    rejection_reason: Optional[str] = None

    class Config:
        from_attributes = True


class LeaveRequestData(BaseModel):
    _id: str
    employee_id: str
    start_date_time: int
    end_date_time: int
    leave_type: int
    duration: int
    status: int
    requested_date: int
    # approval_date: Optional[int] = None
    rejection_reason: str
