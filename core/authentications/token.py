from uuid import UUID

from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from apps.account.models.account import AccountModel
from apps.account.repositories.account import AccountRepository
from apps.auth.schemas.auth import TokenSchema
from core.config.config import config
from exceptions.unauthenticated import UnauthenticatedException
from exceptions.unauthorized import UnauthorizedException
from utils.enums.account_role import AccountRole
from utils.enums.token_type import TokenType


class TokenAuth:
    _ALGORITHM = "HS256"
    _AUTH_JWT_SECRET_KEY = config.AUTH_JWT_SECRET_KEY

    def __init__(self, session: AsyncSession):
        self._session = session

    @classmethod
    def admin_token(cls, _id: UUID, role: AccountRole) -> TokenSchema:
        data = {"id": str(_id), "role": role.value, "type": TokenType.access_token.value}
        token = jwt.encode(data, cls._AUTH_JWT_SECRET_KEY, algorithm=cls._ALGORITHM)
        return TokenSchema(access_token=token)

    def decode(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self._AUTH_JWT_SECRET_KEY, algorithms=[self._ALGORITHM])
            if payload.get("id") is None or payload.get("role") is None or payload.get("type") is None:
                UnauthorizedException.throw()
            return payload.copy()
        except JWTError:
            UnauthenticatedException.throw()

    async def _check_account_is_active(self, account_id: UUID) -> AccountModel:
        account = await AccountRepository(self._session).by_id(_id=account_id)
        if account is None:
            UnauthorizedException.throw()
        elif not account.is_active:
            UnauthorizedException.throw()

        return account

    async def super_admin(self, token: str) -> AccountModel:
        payload = self.decode(token)
        _id = payload.get("id")
        _type = payload.get("role")
        if _id is None or _type is None or _type != AccountRole.super_admin.value:
            UnauthorizedException.throw()
        return await self._check_account_is_active(_id)
