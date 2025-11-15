from apps.auth.schemas.auth import AccountLoginSchema, AdminAuthResponseSchema
from apps.auth.services.auth import AuthService


class AuthController:
    def __init__(self, service: AuthService):
        self._service = service

    async def account_login(self, data: AccountLoginSchema) -> AdminAuthResponseSchema:
        return await self._service.account_login(data)
