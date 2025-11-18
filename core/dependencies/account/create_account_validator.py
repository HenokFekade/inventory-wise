from fastapi import Depends

from apps.account.repositories.account import AccountRepository
from apps.account.schemas.account import CreateAccountSchema
from core.dependencies.account.account_repo import account_repo_dep
from exceptions.unprocessable_entity import UnprocessableEntityException


async def create_account_validator_dep(
        data: CreateAccountSchema,
        repo: AccountRepository = Depends(account_repo_dep),
) -> CreateAccountSchema:
    resp = await repo.by_username(data.username)
    if resp is not None:
        UnprocessableEntityException.throw("username", ["Username already token."])

    resp = await repo.by_phone(data.phone)
    if resp is not None:
        UnprocessableEntityException.throw("phone", ["Phone already token."])

    return data
