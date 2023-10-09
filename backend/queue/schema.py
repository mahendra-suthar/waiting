from datetime import time
from typing import Optional
from pydantic import BaseModel, EmailStr, constr

from ..constants import QUEUE_REGISTERED

employee_collection = 'queue'


class RegisterQueue(BaseModel):
    name: str
    merchant_id: str
    employee_id: str
    limit: int
    start_time: time
    end_time: time
    status: int = QUEUE_REGISTERED

    class Config:
        from_attributes = True


class UpdateQueue(BaseModel):
    name: str
    merchant_id: str
    employee_id: str
    limit: int
    start_time: int
    end_time: int


class QueueData(BaseModel):
    _id: str
    name: str
    merchant_id: str
    employee_id: str
    limit: int
    start_time: int
    end_time: int
