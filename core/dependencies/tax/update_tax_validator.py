from uuid import UUID

from fastapi import Depends, Path

from apps.tax.repositories.tax import TaxRepository
from apps.tax.schemas.tax import UpdateTaxSchema
from core.dependencies.tax.tax_repo import tax_repo_dep
from exceptions.unprocessable_entity import UnprocessableEntityException


async def update_tax_validator_dep(
        data: UpdateTaxSchema,
        _id: UUID = Path(alias="id"),
        repo: TaxRepository = Depends(tax_repo_dep),
) -> UpdateTaxSchema:
    if data.percent:
        result = await repo.by_percent(data.percent)
        if result and result.id != _id:
            UnprocessableEntityException.throw("percent", ["Percent already taken."])
    return data
