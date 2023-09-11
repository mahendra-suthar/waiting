import uuid
from pydantic import BaseModel, EmailStr
from typing import Optional


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

    class Config:
        from_attributes = True
