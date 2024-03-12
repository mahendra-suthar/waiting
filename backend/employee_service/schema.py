from datetime import time
from typing import Optional
from pydantic import BaseModel

employee_service_collection = 'employee_service'


class RegisterEmployeeService(BaseModel):
    service_id: str
    employee_id: str
    description: str
    service_fee: float
    fee_type: int
    start_time: time
    end_time: time
    duration: int

    class Config:
        from_attributes = True


class UpdateEmployeeService(BaseModel):
    service_id: str
    employee_id: str
    description: Optional[str]
    service_fee: float
    fee_type: int
    start_time: int
    end_time: int
    duration: int


class EmployeeServiceData(BaseModel):
    _id: str
    service_id: str
    employee_id: str
    description: Optional[str]
    service_fee: float
    fee_type: int
    start_time: int
    end_time: int
    duration: int


class EmployeeServiceName(BaseModel):
    _id: str
    service_id: str
    employee_id: str
