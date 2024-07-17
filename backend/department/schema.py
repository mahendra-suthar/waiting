from typing import Optional
from pydantic import BaseModel, EmailStr, constr

from ..constants import SERVICE_REGISTERED


class RegisterDepartment(BaseModel):
    merchant_id: str
    name: str
    description: str

    class Config:
        from_attributes = True


# class UpdateService(BaseModel):
#     merchant_id: int
#     name: str
#     description: str
#     status: int
#
#
# class ServiceData(BaseModel):
#     _id: str
#     merchant_id: int
#     name: str
#     description: str
#     status: int