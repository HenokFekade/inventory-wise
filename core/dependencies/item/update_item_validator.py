import asyncio
from typing import List, Dict

from fastapi import Depends

from apps.category.repositories.category import CategoryRepository
from apps.color.repositories.color import ColorRepository
from apps.currency.repositories.currency import CurrencyRepository
from apps.item.schemas.item import UpdateItemSchema
from apps.size.repositories.size import SizeRepository
from apps.tax.repositories.tax import TaxRepository
from apps.unit.repositories.unit import UnitRepository
from core.dependencies.category.category_repo import category_repo_dep
from core.dependencies.color.color_repo import color_repo_dep
from core.dependencies.currency.currency_repo import currency_repo_dep
from core.dependencies.size.size_repo import size_repo_dep
from core.dependencies.tax.tax_repo import tax_repo_dep
from core.dependencies.unit.unit_repo import unit_repo_dep
from exceptions.unprocessable_entities import UnprocessableEntitiesException
from utils.empty_async import empty_async


async def update_item_validator_dep(
        data: UpdateItemSchema,
        category_repo: CategoryRepository = Depends(category_repo_dep),
        currency_repo: CurrencyRepository = Depends(currency_repo_dep),
        color_repo: ColorRepository = Depends(color_repo_dep),
        size_repo: SizeRepository = Depends(size_repo_dep),
        unit_repo: UnitRepository = Depends(unit_repo_dep),
        tax_repo: TaxRepository = Depends(tax_repo_dep),
) -> UpdateItemSchema:
    requests = [
        empty_async() if data.category_id is None else category_repo.by_id(data.category_id),
        empty_async() if data.color_id is None else color_repo.by_id(data.color_id),
        empty_async() if data.size_id is None else size_repo.by_id(data.size_id),
        empty_async() if data.currency_id is None else currency_repo.by_id(data.currency_id),
        empty_async() if data.unit_id is None else unit_repo.by_id(data.unit_id),
        empty_async() if data.tax_id is None else tax_repo.by_id(data.tax_id),
    ]
    response = await asyncio.gather(*requests)
    category = response[0]
    color = response[1]
    size = response[2]
    currency = response[3]
    unit = response[4]
    tax = response[5]

    errors: Dict[str, List[str]] = {}
    if category is None:
        errors["category_id"] = ["Category not found."]
    if data.color_id and color is None:
        errors["color_id"] = ["Color not found."]
    if data.size_id and size is None:
        errors["size_id"] = ["Size not found."]
    if currency is None:
        errors["currency_id"] = ["Currency not found."]
    if unit is None:
        errors["unit_id"] = ["Unit not found."]
    if tax is None:
        errors["tax_id"] = ["Tax not found."]

    if errors:
        UnprocessableEntitiesException.throw(errors)

    return data
