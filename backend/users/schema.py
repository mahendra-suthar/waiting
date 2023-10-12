import re
import uuid
from bson import ObjectId
from typing import Optional
from pydantic import BaseModel, EmailStr, constr, validator

from ..constants import CUSTOMER, DEFAULT_COUNTRY_CODE
from ..queries import filter_data

users_collection = 'users'


class RegisterUser(BaseModel):
    country_code: str = DEFAULT_COUNTRY_CODE
    phone_number: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    address_id: Optional[str] = None
    merchant_id: Optional[str] = None
    employee_id: Optional[str] = None
    date_of_birth: Optional[int] = None
    gender: Optional[int] = None
    user_type: Optional[int] = CUSTOMER

    class Config:
        from_attributes = True


class UpdateUserProfile(BaseModel):
    country_code: str
    phone_number: str
    full_name: str
    email: EmailStr
    address_id: str
    date_of_birth: int
    gender: int

    @validator("country_code")
    def validate_country_code(cls, value):
        if not re.match(r"^\+[1-9]\d*$", value):
            raise ValueError("Invalid country code format")
        return value

    @validator("phone_number", pre=True)
    def validate_mobile(cls, value):
        if not re.match(r"^\d+$", value):
            raise ValueError("Invalid mobile number format")
        return value


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


class UserData(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    full_name: Optional[str]
    phone_number: str
    email: Optional[EmailStr]
    # address_id: Optional[uuid.UUID]
    # merchant_id: Optional[str]
    # employee_id: Optional[str]
    date_of_birth: Optional[int]
    gender: int
    user_type: int
    # is_deleted: Optional[bool] = False

    class Config:
        from_attributes = True
