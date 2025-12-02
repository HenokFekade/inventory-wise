from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel

from apps.store.schemas.store import ItemStoreSchema
from utils.schemas.base_schema import BaseSchema, BaseResponseSchema, BasePaginationResponseSchema, DatabaseSchema


class CreateStoreItemSchema(BaseModel):
    store_id: UUID
    item_id: UUID
    quantity: int


class CreateStoreItemModelSchema(CreateStoreItemSchema):
    pass


class UpdateStoreItemSchema(BaseModel):
    store_id: Optional[UUID] = None
    item_id: Optional[UUID] = None
    quantity: Optional[int] = None


class UpdateStoreItemModelSchema(UpdateStoreItemSchema):
    pass


class StoreItemSchema(BaseSchema):
    store_id: UUID
    item_id: UUID
    quantity: int


class ItemDetailStoreItemSchema(DatabaseSchema):
    id: UUID
    quantity: int
    store: ItemStoreSchema


class StoreItemResponseSchema(BaseResponseSchema):
    data: StoreItemSchema
    status: int = 200
    message: str = "StoreItem fetched successfully"


class StoreItemsResponseSchema(BasePaginationResponseSchema):
    data: List[StoreItemSchema]
    status: int = 200
    message: str = "StoreItems fetched successfully"
