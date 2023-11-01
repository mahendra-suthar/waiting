import re
from pydantic import BaseModel, EmailStr, validator
from typing import Optional

from ..constants import CUSTOMER, DEFAULT_COUNTRY_CODE
from ..queries import filter_data

users_collection = 'users'


class SendOTP(BaseModel):
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

    # @validator('email', pre=True)
    # def check_email_uniqueness(cls, value):
    #     if filter_data(users_collection, {'email': value}):
    #         raise ValueError("Email already exists")
    #     return value
    #
    # @validator('phone_number', pre=True)
    # def check_phone_uniqueness(cls, value):
    #     if filter_data(users_collection, {'phone_number': value}):
    #         raise ValueError("Phone number already exists")
    #     return value


    class Config:
        from_attributes = True


class VerifyOTP(BaseModel):
    country_code: str = DEFAULT_COUNTRY_CODE
    phone_number: str
    otp: int

    class Config:
        from_attributes = True
