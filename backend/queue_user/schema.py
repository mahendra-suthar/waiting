from typing import Optional
from pydantic import BaseModel, EmailStr, constr

from ..constants import QUEUE_USER_REGISTERED

employee_collection = 'queue_user'


class RegisterQueueUser(BaseModel):
    user_id: str
    queue_id: str
    enqueue_time: int
    dequeue_time: int
    priority: bool = False
    status: int = QUEUE_USER_REGISTERED
    service_id: str
    employee_id: str

    class Config:
        from_attributes = True


class UpdateQueueUser(BaseModel):
    user_id: str
    queue_id: str
    enqueue_time: int
    dequeue_time: int
    status: int
    priority: bool


class QueueUserData(BaseModel):
    _id: str
    user_id: str
    queue_id: str
    enqueue_time: int
    dequeue_time: int
    status: int
    priority: bool
