from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, AnyHttpUrl, Field

from utils.schemas.base_schema import BaseSchema, BaseResponseSchema, BasePaginationResponseSchema


class CreateStokeItemSchema(BaseModel):
    store_id: UUID
    quantity: int = Field(gt=0)

class CreateItemSchema(BaseModel):
    name: str
    code: Optional[str] = None
    category_id: UUID
    color_id: Optional[UUID] = None
    size_id: Optional[UUID] = None
    currency_id: UUID
    unit_id: UUID
    tax_id: UUID
    unit_cost: float = Field(gt=0)
    selling_price: float = Field(gt=0)
    min_selling_price: float = Field(gt=0)
    warning_quantity: int = Field(gt=0)
    is_publicly_visible: bool
    description: Optional[str] = None
    images: List[AnyHttpUrl]
    stokes: List[CreateStokeItemSchema] = Field(min_length=1)


class CreateItemModelSchema(BaseModel):
    name: str
    code: Optional[str] = None
    category_id: UUID
    color_id: Optional[UUID] = None
    size_id: Optional[UUID] = None
    currency_id: UUID
    unit_id: UUID
    tax_id: UUID
    unit_cost: float
    selling_price: float
    min_selling_price: float
    warning_quantity: int
    is_publicly_visible: bool
    description: Optional[str] = None
    images: List[AnyHttpUrl]


class UpdateItemSchema(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    category_id: Optional[UUID] = None
    color_id: Optional[UUID] = None
    size_id: Optional[UUID] = None
    currency_id: Optional[UUID] = None
    unit_id: Optional[UUID] = None
    tax_id: Optional[UUID] = None
    unit_cost: Optional[float] = Field(default=None, gt=0)
    selling_price: Optional[float] = Field(default=None, gt=0)
    min_selling_price: Optional[float] = Field(default=None, gt=0)
    warning_quantity: Optional[int] = Field(default=None, gt=0)
    is_publicly_visible: Optional[bool] = None
    description: Optional[str] = None
    images: Optional[List[AnyHttpUrl]] = None


class UpdateItemModelSchema(UpdateItemSchema):
    pass


class ItemSchema(BaseSchema):
    name: str
    code: Optional[str] = None
    category_id: UUID
    color_id: Optional[UUID] = None
    size_id: Optional[UUID] = None
    currency_id: UUID
    unit_id: UUID
    tax_id: UUID
    unit_cost: float = Field(gt=0)
    selling_price: float = Field(gt=0)
    min_selling_price: float = Field(gt=0)
    warning_quantity: int = Field(gt=0)
    is_publicly_visible: bool
    description: Optional[str] = None
    images: List[AnyHttpUrl]

class ItemResponseSchema(BaseResponseSchema):
    data: ItemSchema
    status: int = 200
    message: str = "Item fetched successfully"


class ItemsResponseSchema(BasePaginationResponseSchema):
    data: List[ItemSchema]
    status: int = 200
    message: str = "Items fetched successfully"
