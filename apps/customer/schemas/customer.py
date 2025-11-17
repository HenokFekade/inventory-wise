from typing import Optional, List

from pydantic import BaseModel

from utils.schemas.base_schema import BaseSchema, BaseResponseSchema, BasePaginationResponseSchema


class CreateCustomerSchema(BaseModel):
    name: str
    phone: str
    house_number: str
    country: Optional[str] = None
    city: Optional[str] = None
    note: Optional[str] = None
    additional_phone: Optional[str] = None


class CreateCustomerModelSchema(CreateCustomerSchema):
    pass


class UpdateCustomerSchema(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    house_number: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    note: Optional[str] = None
    additional_phone: Optional[str] = None


class UpdateCustomerModelSchema(UpdateCustomerSchema):
    pass


class CustomerSchema(BaseSchema):
    name: str
    phone: str
    house_number: str
    country: Optional[str] = None
    city: Optional[str] = None
    note: Optional[str] = None
    additional_phone: Optional[str] = None


class CustomerResponseSchema(BaseResponseSchema):
    data: CustomerSchema
    status: int = 200
    message: str = "Customer fetched successfully"


class CustomersResponseSchema(BasePaginationResponseSchema):
    data: List[CustomerSchema]
    status: int = 200
    message: str = "Customers fetched successfully"
