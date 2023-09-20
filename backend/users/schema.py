import re
import uuid
from typing import Optional
from pydantic import BaseModel, EmailStr, constr, validator


class RegisterUser(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    full_name: Optional[str]
    phone_number: constr(min_length=1, max_length=15)
    email: Optional[EmailStr]
    address_id: Optional[uuid.UUID]
    merchant_id: Optional[uuid.UUID]
    employee_id: Optional[uuid.UUID]
    user_type: Optional[int]
    date_of_birth: Optional[int]
    gender: Optional[int]
    is_deleted: Optional[bool] = False

    @validator("phone_number", pre=True)
    def validate_mobile(cls, value):
        if not re.match(r"^\+?[1-9]\d{1,14}$", value):
            raise ValueError("Invalid mobile number format")
        return value

    class Config:
        from_attributes = True


class UpdateUser(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    full_name: Optional[str]
    phone_number: Optional[str]
    email: Optional[EmailStr]
    address_id: Optional[uuid.UUID]
    merchant_id: Optional[uuid.UUID]
    employee_id: Optional[uuid.UUID]
    user_type: Optional[int]
    date_of_birth: Optional[int]
    gender: Optional[int]

    class Config:
        from_attributes = True
