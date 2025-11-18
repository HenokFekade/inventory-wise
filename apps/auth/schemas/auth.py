from pydantic import BaseModel

from apps.account.schemas.account import AccountSchema
from utils.schemas.base_schema import BaseResponseSchema


class TokenSchema(BaseModel):
    access_token: str

class AccountLoginSchema(BaseModel):
    username: str
    password: str

class AdminAuthResponseSchema(BaseResponseSchema):
    data: AccountSchema
    token: TokenSchema
    message: str = "You have successfully logged in"
    status: int = 200
