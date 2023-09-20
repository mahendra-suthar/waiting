import re
import uuid
from typing import Optional
from pydantic import BaseModel, EmailStr, constr, validator


class RegisterBusiness(BaseModel):
    name: str
    email: EmailStr
    country_code: str
    phone: constr(min_length=1, max_length=15)
    password: str
    address_id: Optional[uuid.UUID]
    category_id: Optional[uuid.UUID]
    about_business: Optional[str]
    status: Optional[int]
    email_verify: bool = False
    phone_verify: bool = False
    is_deleted: bool = False

    class Config:
        from_attributes = True

    @validator("phone", pre=True)
    def validate_mobile(cls, value):
        if not re.match(r"^\+?[1-9]\d{1,14}$", value):
            raise ValueError("Invalid mobile number format")
        return value
    # Custom validation for mobile number


class UpdateBusiness(BaseModel):
    name: str
    email: EmailStr
    country_code: str
    phone: constr(min_length=1, max_length=15)
    password: str
    address_id: Optional[uuid.UUID]
    category_id: Optional[uuid.UUID]
    about_business: Optional[str]
    status: Optional[int]

    class Config:
        from_attributes = True
    # Custom validation for mobile number
