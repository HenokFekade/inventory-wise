from uuid import UUID

from fastapi import Depends, Path

from apps.currency.repositories.currency import CurrencyRepository
from apps.currency.schemas.currency import UpdateCurrencySchema
from core.dependencies.currency.currency_repo import currency_repo_dep
from exceptions.unprocessable_entity import UnprocessableEntityException


async def update_currency_validator_dep(
        data: UpdateCurrencySchema,
        _id: UUID = Path(alias="id"),
        repo: CurrencyRepository = Depends(currency_repo_dep),
) -> UpdateCurrencySchema:
    if data.name:
        result = await repo.by_name(data.name)
        if result and result.id == _id:
            UnprocessableEntityException.throw("name", ["Name already taken."])

    if data.code:
        result = await repo.by_code(data.code)
        if result and result.id == _id:
            UnprocessableEntityException.throw("code", ["Code already taken."])
    return data
