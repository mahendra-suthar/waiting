import uuid
from typing import Optional
from pydantic import BaseModel, EmailStr

from ..utils import get_current_timestamp_utc


class RegisterUser(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    full_name: Optional[str]
    phone_number: str
    email: Optional[EmailStr]
    address_id: Optional[uuid.UUID]
    merchant_id: Optional[uuid.UUID]
    employee_id: Optional[uuid.UUID]
    user_type: Optional[int]
    date_of_birth: Optional[int]
    gender: Optional[int]
    is_deleted: Optional[bool] = False
    created_at: Optional[int] = get_current_timestamp_utc()
    created_by: Optional[uuid.UUID]

    class Config:
        from_attributes = True


class UpdateUser(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    full_name: Optional[str]
    phone_number: str
    email: Optional[EmailStr]
    address_id: Optional[uuid.UUID]
    merchant_id: Optional[uuid.UUID]
    employee_id: Optional[uuid.UUID]
    user_type: Optional[int]
    date_of_birth: Optional[int]
    gender: Optional[int]
    updated_at: Optional[int] = get_current_timestamp_utc()
    updated_by: Optional[uuid.UUID]

    class Config:
        from_attributes = True
