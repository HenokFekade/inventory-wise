from typing import Optional
from uuid import UUID

from apps.account.models.account import AccountModel
from apps.account.repositories.account import AccountRepository
from apps.account.schemas.account import AccountsResponseSchema, AccountSchema, AccountResponseSchema, \
    CreateAccountSchema, CreateAccountModelSchema, UpdateAccountSchema, UpdateAccountModelSchema, ChangePasswordSchema
from exceptions.unauthorized import UnauthorizedException
from utils.enums.account_role import AccountRole
from utils.password import PasswordHelper


class AccountService:
    def __init__(self, repo: AccountRepository):
        self._repo = repo

    async def index(
            self,
            account: AccountModel,
            search: str,
            per_page: int,
            page: int,
            role: Optional[AccountRole],
            is_active: Optional[bool],
    ) -> AccountsResponseSchema:
        result, total = await self._repo.by_pagination(
            exclude_id=account.id,
            offset=page,
            search=search,
            is_active=is_active,
            role=role,
            limit=per_page,
        )
        data = [AccountSchema.model_validate(value) for value in result]
        return AccountsResponseSchema(data=data, total=total, page=page, per_page=per_page)

    @staticmethod
    async def by_id(data: AccountModel, account_id: UUID) -> AccountResponseSchema:
        if data.id == account_id:
            UnauthorizedException.throw("You are not authorized get your own information")
        return AccountResponseSchema(data=AccountSchema.model_validate(data))

    async def store(self, data: CreateAccountSchema) -> AccountResponseSchema:
        data.password = PasswordHelper.hash(data.password)
        data = await self._repo.store(CreateAccountModelSchema(**data.model_dump(), password_change_required=False))
        return AccountResponseSchema(
            data=AccountSchema.model_validate(data),
            status=201,
            message="Account created successfully",
        )

    async def update(self, account: AccountModel, data: UpdateAccountSchema) -> AccountResponseSchema:
        data = UpdateAccountModelSchema(**data.model_dump())
        if data.password:
            data.password = PasswordHelper.hash(data.password)
        result = await self._repo.update(data=data, _id=account.id)
        return AccountResponseSchema(
            data=AccountSchema.model_validate(result),
            message="Account updated successfully",
        )

    async def change_password(
            self,
            account: AccountModel,
            data: ChangePasswordSchema,
    ) -> AccountResponseSchema:
        data.password = PasswordHelper.hash(data.password)
        data = UpdateAccountModelSchema(password=data.password, password_change_required=False)
        data = await self._repo.update(data=data, _id=account.id)
        return AccountResponseSchema(
            data=AccountSchema.model_validate(data),
            message="Password changed successfully",
        )

    async def delete(self, data: AccountModel) -> AccountResponseSchema:
        await self._repo.delete(_id=data.id)
        return AccountResponseSchema(
            data=AccountSchema.model_validate(data),
            message="Account deleted successfully",
        )
