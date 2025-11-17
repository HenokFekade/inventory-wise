from typing import Optional, List

from pydantic import BaseModel

from utils.schemas.base_schema import BaseSchema, BaseResponseSchema, BasePaginationResponseSchema


class CreateUnitSchema(BaseModel):
    name: str
    description: Optional[str] = None


class CreateUnitModelSchema(CreateUnitSchema):
    pass


class UpdateUnitSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class UpdateUnitModelSchema(UpdateUnitSchema):
    pass


class UnitSchema(BaseSchema):
    name: str
    description: Optional[str] = None


class UnitResponseSchema(BaseResponseSchema):
    data: UnitSchema
    status: int = 200
    message: str = "Unit fetched successfully"


class UnitsResponseSchema(BasePaginationResponseSchema):
    data: List[UnitSchema]
    status: int = 200
    message: str = "Units fetched successfully"
