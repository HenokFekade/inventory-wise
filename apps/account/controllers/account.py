from typing import Optional

from apps.account.models.account import AccountModel
from apps.account.schemas.account import AccountsResponseSchema, AccountResponseSchema, CreateAccountSchema, \
    UpdateAccountSchema
from apps.account.services.account import AccountService
from utils.enums.account_role import AccountRole


class AccountController:
    def __init__(self, service: AccountService):
        self._service = service

    async def index(
            self,
            account: AccountModel,
            search: str,
            per_page: int,
            page: int,
            role: Optional[AccountRole],
            is_active: Optional[bool],
    ) -> AccountsResponseSchema:
        return await self._service.index(
            is_active=is_active,
            search=search,
            role=role,
            account=account,
            per_page=per_page,
            page=page,
        )

    async def by_id(self, account: AccountModel) -> AccountResponseSchema:
        return await self._service.by_id(account)

    async def store(self, data: CreateAccountSchema) -> AccountResponseSchema:
        return await self._service.store(data)

    async def update(self, account: AccountModel, data: UpdateAccountSchema) -> AccountResponseSchema:
        return await self._service.update(data=data, account=account)

    async def delete(self, data: AccountModel) -> AccountResponseSchema:
        return await self._service.delete(data)
