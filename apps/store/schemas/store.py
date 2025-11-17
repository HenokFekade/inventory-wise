from typing import Optional, List

from pydantic import BaseModel

from utils.schemas.base_schema import BaseSchema, BaseResponseSchema, BasePaginationResponseSchema


class CreateStoreSchema(BaseModel):
    name: str
    description: Optional[str] = None


class CreateStoreModelSchema(CreateStoreSchema):
    pass


class UpdateStoreSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class UpdateStoreModelSchema(UpdateStoreSchema):
    pass


class StoreSchema(BaseSchema):
    name: str
    description: Optional[str] = None


class StoreResponseSchema(BaseResponseSchema):
    data: StoreSchema
    status: int = 200
    message: str = "Store fetched successfully"


class StoresResponseSchema(BasePaginationResponseSchema):
    data: List[StoreSchema]
    status: int = 200
    message: str = "Stores fetched successfully"
