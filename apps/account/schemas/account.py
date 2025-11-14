from typing import Optional, List

from pydantic import BaseModel, EmailStr

from utils.enums.account_role import AccountRole
from utils.schemas.base_schema import BaseSchema, BaseResponseSchema, BasePaginationResponseSchema


class CreateAccountSchema(BaseModel):
    first_name: str
    last_name: str
    role: AccountRole
    phone: str
    email: EmailStr
    image: Optional[str] = None
    password: str

class CreateAccountModelSchema(CreateAccountSchema):
    pass

class UpdateAccountSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: AccountRole
    phone: Optional[str] = None
    email: EmailStr
    image: Optional[str] = None
    password: Optional[str] = None

class UpdateAccountModelSchema(UpdateAccountSchema):
    pass

class AccountSchema(BaseSchema):
    first_name: str
    last_name: str
    role: AccountRole
    phone: str
    email: EmailStr
    image: Optional[str] = None
    password_change_required: bool

class AccountResponseSchema(BaseResponseSchema):
    data: AccountSchema
    status: int = 200
    message: str = "Account fetched successfully"

class AccountsResponseSchema(BasePaginationResponseSchema):
    data: List[AccountSchema]
    status: int = 200
    message: str = "Accounts fetched successfully"
