from fastapi import Depends

from apps.category.repositories.category import CategoryRepository
from apps.color.repositories.color import ColorRepository
from apps.currency.repositories.currency import CurrencyRepository
from apps.item.repositories.item import ItemRepository
from apps.item.services.item import ItemService
from apps.size.repositories.size import SizeRepository
from apps.store_item.repositories.store_item import StoreItemRepository
from apps.tax.repositories.tax import TaxRepository
from apps.unit.repositories.unit import UnitRepository
from core.dependencies.category.category_repo import category_repo_dep
from core.dependencies.color.color_repo import color_repo_dep
from core.dependencies.currency.currency_repo import currency_repo_dep
from core.dependencies.item.item_repo import item_repo_dep
from core.dependencies.size.size_repo import size_repo_dep
from core.dependencies.store_item.store_item_repo import store_item_repo_dep
from core.dependencies.tax.tax_repo import tax_repo_dep
from core.dependencies.unit.unit_repo import unit_repo_dep


def item_service_dep(
        repo: ItemRepository = Depends(item_repo_dep),
        _store_item_repo: StoreItemRepository = Depends(store_item_repo_dep),
        _category_repo: CategoryRepository = Depends(category_repo_dep),
        _color_repo: ColorRepository = Depends(color_repo_dep),
        _size_repo: SizeRepository = Depends(size_repo_dep),
        _currency_repo: CurrencyRepository = Depends(currency_repo_dep),
        _unit_repo: UnitRepository = Depends(unit_repo_dep),
        _tax_repo: TaxRepository = Depends(tax_repo_dep),
) -> ItemService:
    return ItemService(
        category_repo=_category_repo,
        color_repo=_color_repo,
        size_repo=_size_repo,
        currency_repo=_currency_repo,
        unit_repo=_unit_repo,
        tax_repo=_tax_repo,
        repo=repo,
        store_item_repo=_store_item_repo,
    )
