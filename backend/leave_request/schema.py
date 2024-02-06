from typing import Optional
from pydantic import BaseModel, EmailStr, constr

from ..constants import QUEUE_USER_REGISTERED


class RegisterLeaveType(BaseModel):
    business_id: str
    Name: str
    Description: str


class RegisterLeaveRequest(BaseModel):
    employee_id: str
    start_date: int
    end_date: int
    start_duration: int
    end_duration: int
    leave_type: int = 1
    note: str
    duration: int
    status: int = 1
    requested_date: int
    action_date: Optional[int] = None
    action_comment: Optional[str] = None
    action_by: Optional[str] = None

    class Config:
        from_attributes = True


class LeaveRequestActions(BaseModel):
    status: int
    action_comment: Optional[str] = None

    class Config:
        from_attributes = True


class LeaveRequestData(BaseModel):
    _id: str
    employee_id: str
    start_date: int
    end_date: int
    leave_type: int
    duration: int
    status: int
    note: str
    requested_date: int
    # action_date: int
    # action_comment: str
    # action_by: str
