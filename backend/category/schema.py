from typing import Optional
from pydantic import BaseModel

category_collection = 'category'


class RegisterCategory(BaseModel):
    name: str
    description: str
    parent_category_id: Optional[str]
    is_deleted: Optional[bool] = False

    class Config:
        from_attributes = True


class UpdateCategory(BaseModel):
    name: str
    description: str
    parent_category_id: Optional[str]


class CategoryData(BaseModel):
    _id: str
    name: str
    description: str
    parent_category_id: str


class ParentCategory(BaseModel):
    name: str

