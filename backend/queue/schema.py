from datetime import time
from typing import Optional
from pydantic import BaseModel, EmailStr, constr

from ..constants import QUEUE_REGISTERED, QUEUE_RUNNING_STOP

employee_collection = 'queue'


class RegisterQueue(BaseModel):
    name: str
    # merchant_id: str
    # employee_id: str
    limit: int
    current_user: str = None
    current_length: int = 0
    start_time: time
    end_time: time
    status: int = QUEUE_REGISTERED
    running_status: int = QUEUE_RUNNING_STOP
    last_token_number: int = 0

    class Config:
        from_attributes = True

    def generate_token_number(self) -> str:
        self.last_token_number = (self.last_token_number % 9999) + 1
        return f"{self.last_token_number:04d}"


class UpdateQueue(BaseModel):
    name: str
    # merchant_id: str
    # employee_id: str
    limit: int
    current_user: str
    current_length: int
    start_time: int
    end_time: int


class QueueData(BaseModel):
    _id: str
    name: str
    # merchant_id: str
    # employee_id: str
    limit: int
    current_user: str
    current_length: int
    start_time: int
    end_time: int
    running_status: int
    last_token_number: int
