from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class DatabaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class BaseSchema(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class BaseResponseSchema(BaseModel):
    message: str
    status: int


class BasePaginationResponseSchema(BaseModel):
    message: str
    status: int
    total: int
    page: int
    per_page: int
