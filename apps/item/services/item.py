import asyncio
from typing import List

from apps.category.repositories.category import CategoryRepository
from apps.color.repositories.color import ColorRepository
from apps.currency.repositories.currency import CurrencyRepository
from apps.item.models.item import ItemModel
from apps.item.repositories.item import ItemRepository
from apps.item.schemas.item import ItemsResponseSchema, ItemSchema, ItemResponseSchema, \
    CreateItemSchema, CreateItemModelSchema, UpdateItemSchema, UpdateItemModelSchema, ItemFormResponseSchema, \
    ItemFormSchema
from apps.size.repositories.size import SizeRepository
from apps.store.repositories.store import StoreRepository
from apps.store_item.repositories.store_item import StoreItemRepository
from apps.store_item.schemas.store_item import CreateStoreItemModelSchema
from apps.tax.repositories.tax import TaxRepository
from apps.unit.repositories.unit import UnitRepository
from exceptions.bad_request import BadRequestException


class ItemService:
    def __init__(
            self,
            category_repo: CategoryRepository,
            color_repo: ColorRepository,
            size_repo: SizeRepository,
            store_repo: StoreRepository,
            currency_repo: CurrencyRepository,
            unit_repo: UnitRepository,
            tax_repo: TaxRepository,
            repo: ItemRepository,
            store_item_repo: StoreItemRepository,
    ):
        self._category_repo = category_repo
        self._color_repo = color_repo
        self._size_repo = size_repo
        self._store_repo = store_repo
        self._currency_repo = currency_repo
        self._unit_repo = unit_repo
        self._tax_repo = tax_repo
        self._repo = repo
        self._store_item_repo = store_item_repo

    async def form(self) -> ItemFormResponseSchema:
        categories, colors, sizes, stores, currencies, units, taxes = await asyncio.gather(
            self._category_repo.all(),
            self._color_repo.all(),
            self._size_repo.all(),
            self._store_repo.all(),
            self._currency_repo.all(),
            self._unit_repo.all(),
            self._tax_repo.all(),
        )
        if None in [categories, colors, sizes, currencies, units, taxes]:
            BadRequestException.throw("Something went wrong please try again.")

        data = ItemFormSchema(
            categories=categories,
            colors=colors,
            sizes=sizes,
            stores=stores,
            currencies=currencies,
            units=units,
            taxes=taxes,
        )
        return ItemFormResponseSchema(data=data)

    async def index(self, search: str, per_page: int, page: int) -> ItemsResponseSchema:
        result, total = await self._repo.by_pagination(offset=page, search=search, limit=per_page)
        data = [ItemSchema.model_validate(value) for value in result]
        return ItemsResponseSchema(data=data, total=total, page=page, per_page=per_page)

    async def by_id(self, data: ItemModel) -> ItemResponseSchema:
        data = await self._repo.by_id_with_all_relation_except_store(data.id)
        return ItemResponseSchema(data=ItemSchema.model_validate(data))

    async def store(self, data: CreateItemSchema) -> ItemResponseSchema:
        try:
            data_model = CreateItemModelSchema(**data.model_dump())
            item = await self._repo.store(data=data_model, commit=False)
            store_items: List[CreateStoreItemModelSchema] = []
            store_ids = []
            for store in data.stokes:
                if store.store_id not in store_ids:
                    store_items.append(CreateStoreItemModelSchema(item_id=item.id, **store.model_dump()))
                    store_ids.append(store.store_id)
            await self._store_item_repo.bulk_store(data=store_items, commit=False)
            await self._repo.commit()
            item = await self._repo.by_id_with_all_relation_except_store(item.id)
            return ItemResponseSchema(
                data=ItemSchema.model_validate(item),
                status=201,
                message="Item created successfully",
            )
        except Exception as e:
            print("Something went wrong during item creating", e)
            await self._repo.rollback()
            BadRequestException.throw("Something went wrong during creating items. Please retry again.")

    async def update(self, item: ItemModel, data: UpdateItemSchema) -> ItemResponseSchema:
        data = UpdateItemModelSchema(**data.model_dump())
        result = await self._repo.update(data=data, _id=item.id)
        return ItemResponseSchema(
            data=ItemSchema.model_validate(result),
            message="Item updated successfully",
        )

    async def delete(self, data: ItemModel) -> ItemResponseSchema:
        await self._repo.delete(_id=data.id)
        return ItemResponseSchema(
            data=ItemSchema.model_validate(data),
            message="Item deleted successfully",
        )
