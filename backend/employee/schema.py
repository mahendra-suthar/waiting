import re
import uuid
from typing import Optional
from pydantic import BaseModel, EmailStr, constr, validator


class RegisterEmployee(BaseModel):
    merchant_id: str
    joined_date: int
    department_id: uuid.UUID
    status: int
    email: EmailStr
    country_code: str
    phone_number: constr(min_length=1, max_length=15)
    employee_number: int
    is_deleted: Optional[bool] = False

    @validator("phone_number", pre=True)
    def validate_mobile(cls, value):
        if not re.match(r"^\+?[1-9]\d{1,14}$", value):
            raise ValueError("Invalid mobile number format")
        return value

    class Config:
        from_attributes = True
