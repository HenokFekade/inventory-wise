from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel

from utils.schemas.base_schema import BaseSchema, BaseResponseSchema, BasePaginationResponseSchema, DatabaseSchema


class CreateColorSchema(BaseModel):
    name: str


class CreateColorModelSchema(CreateColorSchema):
    pass


class UpdateColorSchema(BaseModel):
    name: Optional[str] = None


class UpdateColorModelSchema(UpdateColorSchema):
    pass


class ColorSchema(BaseSchema):
    name: str


class ItemColorSchema(DatabaseSchema):
    id: UUID
    name: str


class ColorResponseSchema(BaseResponseSchema):
    data: ColorSchema
    status: int = 200
    message: str = "Color fetched successfully"


class ColorsResponseSchema(BasePaginationResponseSchema):
    data: List[ColorSchema]
    status: int = 200
    message: str = "Colors fetched successfully"
