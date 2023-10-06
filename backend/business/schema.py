import re
import uuid
from typing import Optional
from pydantic import BaseModel, EmailStr, constr, validator

from ..constants import BUSINESS_REGISTERED

business_collection = 'business'


class RegisterBusiness(BaseModel):
    name: str
    email: EmailStr
    country_code: str
    phone_number: str
    password: str
    address_id: Optional[str]
    category_id: Optional[str]
    about_business: Optional[str]
    status: Optional[int] = BUSINESS_REGISTERED
    email_verify: bool = False
    phone_verify: bool = False
    is_deleted: bool = False

    class Config:
        from_attributes = True


class UpdateBusiness(BaseModel):
    name: str
    email: EmailStr
    country_code: str
    phone_number: constr(min_length=1, max_length=15)
    password: str
    address_id: Optional[str]
    category_id: Optional[str]
    about_business: Optional[str]

    class Config:
        from_attributes = True
    # Custom validation for mobile number


class BusinessData(BaseModel):
    _id: str
    name: str
    email: EmailStr
    country_code: str
    phone: str
    password: str
    address_id: str
    category_id: str
    about_business: str
    status: int
