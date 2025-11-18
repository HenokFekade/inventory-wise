from apps.account.repositories.account import AccountRepository
from apps.account.schemas.account import AccountSchema
from apps.auth.schemas.auth import AdminAuthResponseSchema, AccountLoginSchema
from core.authentications.token import TokenAuth
from exceptions.bad_request import BadRequestException
from utils.password import PasswordHelper


class AuthService:
    def __init__(self, account_repo: AccountRepository):
        self._account_repo = account_repo

    async def account_login(self, data: AccountLoginSchema) -> AdminAuthResponseSchema:
        account = await self._account_repo.by_username(data.username)
        if account is None:
            BadRequestException.throw("Invalid username or password")
        if not PasswordHelper.verify(data.password, account.password):
            BadRequestException.throw("Invalid username or password")
        if not account.is_active:
            BadRequestException.throw("Account is not active. Please contact admin.")
        token = TokenAuth.admin_token(role=account.role, _id=account.id)
        return AdminAuthResponseSchema(
            data=AccountSchema.model_validate(account),
            token=token
        )
