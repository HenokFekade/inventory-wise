from uuid import UUID

from fastapi import Depends, Path

from apps.account.repositories.account import AccountRepository
from apps.account.schemas.account import UpdateAccountSchema
from core.dependencies.account.account_repo import account_repo_dep
from exceptions.unprocessable_entity import UnprocessableEntityException


async def update_account_validator_dep(
        data: UpdateAccountSchema,
        _id: UUID = Path(alias="id"),
        repo: AccountRepository = Depends(account_repo_dep),
) -> UpdateAccountSchema:
    if data.username:
        resp = await repo.by_username(data.username)
        if resp is not None and resp.id != _id:
            UnprocessableEntityException.throw("username", ["Username already token."])

    if data.phone:
        resp = await repo.by_phone(data.phone)
        if resp is not None and resp.id != _id:
            UnprocessableEntityException.throw("phone", ["Phone already token."])

    return data
