from typing import Optional, List

from pydantic import BaseModel, Field

from utils.schemas.base_schema import BaseSchema, BaseResponseSchema, BasePaginationResponseSchema


class CreateTaxSchema(BaseModel):
    percent: int = Field(gt=0, le=100)
    description: Optional[str] = None


class CreateTaxModelSchema(CreateTaxSchema):
    pass


class UpdateTaxSchema(BaseModel):
    percent: Optional[int] = Field(gt=0, le=100, default=None)
    description: Optional[str] = None


class UpdateTaxModelSchema(UpdateTaxSchema):
    pass


class TaxSchema(BaseSchema):
    percent: int
    description: Optional[str] = None


class TaxResponseSchema(BaseResponseSchema):
    data: TaxSchema
    status: int = 200
    message: str = "Tax fetched successfully"


class TaxsResponseSchema(BasePaginationResponseSchema):
    data: List[TaxSchema]
    status: int = 200
    message: str = "Taxs fetched successfully"
