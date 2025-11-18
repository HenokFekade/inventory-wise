from typing import Optional, List

from pydantic import BaseModel

from utils.schemas.base_schema import BaseSchema, BaseResponseSchema, BasePaginationResponseSchema


class CreateItemSchema(BaseModel):
    pass


class CreateItemModelSchema(CreateItemSchema):
    pass


class UpdateItemSchema(BaseModel):
    pass


class UpdateItemModelSchema(UpdateItemSchema):
    pass


class ItemSchema(BaseSchema):
    pass


class ItemResponseSchema(BaseResponseSchema):
    data: ItemSchema
    status: int = 200
    message: str = "Item fetched successfully"


class ItemsResponseSchema(BasePaginationResponseSchema):
    data: List[ItemSchema]
    status: int = 200
    message: str = "Items fetched successfully"
