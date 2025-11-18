from fastapi import Depends

from apps.tax.repositories.tax import TaxRepository
from apps.tax.schemas.tax import CreateTaxSchema
from core.dependencies.tax.tax_repo import tax_repo_dep
from exceptions.unprocessable_entity import UnprocessableEntityException


async def create_tax_validator_dep(
        data: CreateTaxSchema,
        repo: TaxRepository = Depends(tax_repo_dep),
) -> CreateTaxSchema:
    result = await repo.by_percent(data.percent)
    if result:
        UnprocessableEntityException.throw("percent", ["Percent already taken."])
    return data
