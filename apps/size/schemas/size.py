from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel

from utils.schemas.base_schema import BaseSchema, BaseResponseSchema, BasePaginationResponseSchema, DatabaseSchema


class CreateSizeSchema(BaseModel):
    name: str
    description: Optional[str] = None


class CreateSizeModelSchema(CreateSizeSchema):
    pass


class UpdateSizeSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class UpdateSizeModelSchema(UpdateSizeSchema):
    pass


class SizeSchema(BaseSchema):
    name: str
    description: Optional[str] = None


class ItemSizeSchema(DatabaseSchema):
    id: UUID
    name: str
    description: Optional[str] = None


class SizeResponseSchema(BaseResponseSchema):
    data: SizeSchema
    status: int = 200
    message: str = "Size fetched successfully"


class SizesResponseSchema(BasePaginationResponseSchema):
    data: List[SizeSchema]
    status: int = 200
    message: str = "Sizes fetched successfully"
