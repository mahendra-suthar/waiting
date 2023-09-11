from pydantic import BaseModel, Field


class BaseCommonModel(BaseModel):
    """
    This is User table also we can represent it as customer
    """
    created_at: int = Field(..., description="entry inserted at")
    created_by: str = Field(..., description="entry inserted by (user's id)")
    updated_at: int = Field(..., description="entry updated at")
    updated_by: str = Field(..., description="entry updated by (user's id)")
    is_deleted: bool = Field(False, description="soft delete")
