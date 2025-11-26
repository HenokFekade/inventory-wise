from typing import Optional, List

from pydantic import BaseModel, field_validator, ValidationInfo, AnyHttpUrl

from utils.enums.account_role import AccountRole
from utils.schemas.base_schema import BaseSchema, BaseResponseSchema, BasePaginationResponseSchema


class CreateAccountSchema(BaseModel):
    first_name: str
    last_name: str
    role: AccountRole
    phone: str
    username: str
    image: Optional[AnyHttpUrl] = None
    password: str

    # @field_validator('phone')
    # @classmethod
    # def check_phone_is_ethiopian(cls, v: str) -> str:
    #     if not re.match(r"^(\+251|0|251)([97])[0-9]{8}$", v):
    #         raise ValueError("Invalid ethiopian phone number")
    #     # replace +251 or 251 or 0 to +251
    #     v = re.sub(r"^(\+251|0|251)", "+251", v)
    #     return v

class CreateAccountModelSchema(CreateAccountSchema):
    password_change_required: bool

class UpdateAccountSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[AccountRole] = None
    phone: Optional[str] = None
    username: Optional[str] = None
    image: Optional[AnyHttpUrl] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

    # @field_validator('phone')
    # @classmethod
    # def check_phone_is_ethiopian(cls, v: Optional[str]) -> Optional[str]:
    #     if v is None:
    #         return v
    #     if not re.match(r"^(\+251|0|251)([97])[0-9]{8}$", v):
    #         raise ValueError("Invalid ethiopian phone number")
    #     # replace +251 or 251 or 0 to +251
    #     v = re.sub(r"^(\+251|0|251)", "+251", v)
    #     return v

class UpdateAccountModelSchema(UpdateAccountSchema):
    password_change_required: Optional[bool] = None


class ChangePasswordSchema(BaseModel):
    password: str
    new_password: str
    confirm_password: str

    @field_validator('confirm_password')
    @classmethod
    def check_confirm_password(cls, v: str, values: ValidationInfo) -> str:
        if v != values.data.get('new_password'):
            raise ValueError("Passwords do not match")
        return v

class AccountSchema(BaseSchema):
    first_name: str
    last_name: str
    role: AccountRole
    phone: str
    username: str
    image: Optional[AnyHttpUrl] = None
    password_change_required: bool
    is_active: bool

class AccountResponseSchema(BaseResponseSchema):
    data: AccountSchema
    status: int = 200
    message: str = "Account fetched successfully"

class AccountsResponseSchema(BasePaginationResponseSchema):
    data: List[AccountSchema]
    status: int = 200
    message: str = "Accounts fetched successfully"
