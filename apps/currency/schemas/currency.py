from typing import Optional, List

from pydantic import BaseModel

from utils.schemas.base_schema import BaseSchema, BaseResponseSchema, BasePaginationResponseSchema


class CreateCurrencySchema(BaseModel):
    name: str
    code: str


class CreateCurrencyModelSchema(CreateCurrencySchema):
    pass


class UpdateCurrencySchema(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None


class UpdateCurrencyModelSchema(UpdateCurrencySchema):
    pass


class CurrencySchema(BaseSchema):
    name: str
    code: str


class CurrencyResponseSchema(BaseResponseSchema):
    data: CurrencySchema
    status: int = 200
    message: str = "Currency fetched successfully"


class CurrenciesResponseSchema(BasePaginationResponseSchema):
    data: List[CurrencySchema]
    status: int = 200
    message: str = "Currencies fetched successfully"
