from typing import Optional, List

from pydantic import BaseModel

from utils.schemas.base_schema import BaseSchema, BaseResponseSchema, BasePaginationResponseSchema


class CreateSupplierSchema(BaseModel):
    name: str
    phone: str
    address: Optional[str] = None
    note: Optional[str] = None


class CreateSupplierModelSchema(CreateSupplierSchema):
    pass


class UpdateSupplierSchema(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    note: Optional[str] = None


class UpdateSupplierModelSchema(UpdateSupplierSchema):
    pass


class SupplierSchema(BaseSchema):
    name: str
    phone: str
    address: Optional[str] = None
    note: Optional[str] = None


class SupplierResponseSchema(BaseResponseSchema):
    data: SupplierSchema
    status: int = 200
    message: str = "Supplier fetched successfully"


class SuppliersResponseSchema(BasePaginationResponseSchema):
    data: List[SupplierSchema]
    status: int = 200
    message: str = "Suppliers fetched successfully"
