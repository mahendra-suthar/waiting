from pydantic import BaseModel


class RegisterLeaveType(BaseModel):
    business_id: str
    name: str
    description: str


class LeaveTypeData(BaseModel):
    business_id: str
    name: str
    description: str


class RegisterLeaveBalance(BaseModel):
    employee_id: str
    leave_type_id: str
    leave_year: int
    entitlement: int
    consumed: int
    available: int


class LeaveBalanceData(BaseModel):
    employee_id: str
    leave_type_id: str
    leave_year: str
    entitlement: int
    consumed: int
    available: int

