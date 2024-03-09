from pydantic import BaseModel
from datetime import time

category_collection = 'business_schedule'


class RegisterBusinessSchedule(BaseModel):
    merchant_id: str
    day_of_week: int
    opening_time: time = None
    closing_time: time = None
    is_open: bool = False

    class Config:
        from_attributes = True


class UpdateBusinessSchedule(BaseModel):
    merchant_id: str
    day_of_week: int
    opening_time: time
    closing_time: time


class BusinessScheduleData(BaseModel):
    _id: str
    merchant_id: str
    day_of_week: int
    opening_time: time
    closing_time: time

