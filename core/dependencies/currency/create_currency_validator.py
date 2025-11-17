from fastapi import Depends

from apps.currency.repositories.currency import CurrencyRepository
from apps.currency.schemas.currency import CreateCurrencySchema
from core.dependencies.currency.currency_repo import currency_repo_dep
from exceptions.unprocessable_entity import UnprocessableEntityException


async def create_currency_validator_dep(
        data: CreateCurrencySchema,
        repo: CurrencyRepository = Depends(currency_repo_dep),
) -> CreateCurrencySchema:
    result = await repo.by_name(data.name)
    if result:
        UnprocessableEntityException.throw("name", ["Name already taken."])

    result = await repo.by_code(data.code)
    if result:
        UnprocessableEntityException.throw("code", ["Code already taken."])

    return data
