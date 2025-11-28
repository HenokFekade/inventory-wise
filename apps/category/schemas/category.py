from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, AnyHttpUrl

from utils.schemas.base_schema import BaseSchema, BaseResponseSchema, BasePaginationResponseSchema, DatabaseSchema


class CreateCategorySchema(BaseModel):
    name: str
    category_id: Optional[UUID] = None
    images: Optional[List[AnyHttpUrl]] = None
    is_active: Optional[bool] = True
    is_publicly_visible: bool


class CreateCategoryModelSchema(CreateCategorySchema):
    pass


class UpdateCategorySchema(BaseModel):
    name: Optional[str] = None
    category_id: Optional[UUID] = None
    images: Optional[List[AnyHttpUrl]] = None
    is_active: Optional[bool] = None
    is_publicly_visible: Optional[bool] = None


class UpdateCategoryModelSchema(UpdateCategorySchema):
    pass


class CategorySchema(BaseSchema):
    name: str
    category_id: Optional[UUID] = None
    images: Optional[List[AnyHttpUrl]] = None
    is_active: bool
    is_publicly_visible: bool


class ItemCategorySchema(DatabaseSchema):
    id: UUID
    name: str
    images: Optional[List[AnyHttpUrl]] = None


class CategoryResponseSchema(BaseResponseSchema):
    data: CategorySchema
    status: int = 200
    message: str = "Category fetched successfully"


class CategoriesResponseSchema(BasePaginationResponseSchema):
    data: List[CategorySchema]
    status: int = 200
    message: str = "Categories fetched successfully"
