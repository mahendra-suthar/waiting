from typing import Optional
from pydantic import BaseModel, EmailStr, constr

post_collection = 'post'


class RegisterPost(BaseModel):
    business_id: str
    title: str
    image: str
    content: str
    post_type: int

    class Config:
        from_attributes = True


class PostData(BaseModel):
    title: str
    image: str
    content: str
    post_type: int