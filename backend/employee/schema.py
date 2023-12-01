import re
import uuid
from typing import Optional
from pydantic import BaseModel, EmailStr, constr, validator

from ..constants import EMPLOYEE_REGISTERED
employee_collection = 'employee'


class RegisterEmployee(BaseModel):
    merchant_id: str
    joined_date: int
    department_id: str
    # status: int
    email: EmailStr
    country_code: constr(min_length=1, max_length=4)
    phone_number: constr(min_length=1, max_length=15)
    employee_number: int
    email_verify: bool = False
    phone_verify: bool = False
    status: int = EMPLOYEE_REGISTERED
    user_id: str
    queue_id: str

    # @validator("country_code")
    # def validate_country_code(cls, value):
    #     if not re.match(r"^\+[1-9]\d*$", value):
    #         raise ValueError("Invalid country code format")
    #     return value
    #
    # @validator("phone_number", pre=True)
    # def validate_mobile(cls, value):
    #     if not re.match(r"^\d+$", value):
    #         raise ValueError("Invalid mobile number format")
    #     return value
    #
    # @validator('email', pre=True)
    # def check_email_uniqueness(cls, value):
    #     if filter_data(employee_collection, {'email': value}):
    #         raise ValueError("Email already exists")
    #     return value
    #
    # @validator('phone_number', pre=True)
    # def check_phone_uniqueness(cls, value):
    #     if filter_data(employee_collection, {'phone_number': value}):
    #         raise ValueError("Phone number already exists")
    #     return value

    class Config:
        from_attributes = True


class UpdateEmployee(BaseModel):
    merchant_id: str
    joined_date: int
    department_id: str
    # status: int
    email: EmailStr
    country_code: constr(min_length=1, max_length=4)
    phone_number: constr(min_length=1, max_length=15)
    employee_number: int
    queue_id: str


class EmployeeData(BaseModel):
    _id: str
    merchant_id: str
    joined_date: int
    status: int
    email: str
    country_code: str
    phone_number: str
    employee_number: int
    queue_id: str
