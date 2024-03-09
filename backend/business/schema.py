import re
import uuid
from typing import Optional
from pydantic import BaseModel, EmailStr, constr, validator

from ..constants import BUSINESS_REGISTERED

business_collection = 'business'


class RegisterBusiness(BaseModel):
    name: str
    email: EmailStr = None
    country_code: str
    phone_number: str
    password: Optional[str] = None
    address_id: Optional[str] = None
    category_id: str
    about_business: Optional[str] = None
    status: Optional[int] = BUSINESS_REGISTERED
    email_verify: bool = False
    phone_verify: bool = False
    owner_id: str
    qr_code: str = None
    schedule_list: list = []

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
    qr_code: str
    status: int
