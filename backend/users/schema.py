import re
import uuid
from typing import Optional
from pydantic import BaseModel, EmailStr, constr, validator

from ..constants import CUSTOMER, MALE


class RegisterUser(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    full_name: Optional[str]
    phone_number: str
    email: Optional[EmailStr]
    # address_id: Optional[uuid.UUID]
    # merchant_id: Optional[str]
    # employee_id: Optional[str]
    date_of_birth: Optional[int]
    gender: int = MALE
    user_type: Optional[int] = CUSTOMER
    is_deleted: Optional[bool] = False

    class Config:
        from_attributes = True


class UpdateUser(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    full_name: Optional[str]
    phone_number: Optional[str]
    email: Optional[EmailStr]
    # address_id: Optional[uuid.UUID]
    # merchant_id: Optional[uuid.UUID]
    # employee_id: Optional[uuid.UUID]
    # user_type: Optional[int]
    date_of_birth: Optional[int]
    # gender: Optional[int]

    class Config:
        from_attributes = True
