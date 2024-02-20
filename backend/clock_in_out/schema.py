from pydantic import BaseModel, EmailStr, constr

from ..utils import get_current_timestamp_utc
employee_collection = 'employee'


class RegisterAttendance(BaseModel):
    employee_id: str
    event_type: int
    timestamp: int

    class Config:
        from_attributes = True


class AttendanceData(BaseModel):
    _id: str
    employee_id: str
    event_type: int
    timestamp: int
