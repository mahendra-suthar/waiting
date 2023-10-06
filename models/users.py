import uuid
from datetime import date
from typing import Optional
from enum import Enum as PyEnum
from pydantic import Field, EmailStr

from .base import BaseCommonModel


class UserType(str, PyEnum):
    customer = 1
    merchant = 2
    employee = 3


class User(BaseCommonModel):
    """
    This is User table also we can represent it as customer
    """
    id: Optional[str] = Field(default_factory=uuid.uuid4, alias="_id")
    first_name: Optional[str] = Field(..., description="user's first name")
    last_name: Optional[str] = Field(..., description="user's last name")
    full_name: Optional[str] = Field(..., description="combination of first_name and last_name.")
    phone_number: str = Field(..., description="user's phone number")
    email: Optional[EmailStr] = Field(..., description="user's email")
    address_id: Optional[str] = Field(..., description="user's address (reference from address table)")
    merchant_id: Optional[str] = Field(..., description="user's business (reference from merchant table)")
    employee_id: Optional[str] = Field(
        description="If user is employee then here will be employee's id from employee table"
    )
    user_type: UserType = Field(UserType.customer, description="The type of user.")
    date_of_birth: Optional[date] = Field(..., description="The date of birth of the user in YYYY-MM-DD format.")
    phone_number_verify: Optional[bool] = Field(
        False,
        description="This field is defined phone number is verify or not"
    )
    email_verify: Optional[bool] = Field(False, description="This field is defined email is verify or not")
    gender: Optional[int] = Field(..., description="user's first name")
