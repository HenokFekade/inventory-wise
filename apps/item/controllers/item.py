from apps.item.models.item import ItemModel
from apps.item.schemas.item import ItemsResponseSchema, ItemResponseSchema, CreateItemSchema, \
    UpdateItemSchema, ItemFormResponseSchema, ItemDetailResponseSchema
from apps.item.services.item import ItemService


class ItemController:
    def __init__(self, service: ItemService):
        self._service = service

    async def index(self, search: str, per_page: int, page: int) -> ItemsResponseSchema:
        return await self._service.index(search=search, per_page=per_page, page=page)

    async def form(self) -> ItemFormResponseSchema:
        return await self._service.form()

    async def by_id(self, item: ItemModel) -> ItemResponseSchema:
        return await self._service.by_id(data=item)

    async def detail_by_id(self, item: ItemModel) -> ItemDetailResponseSchema:
        return await self._service.detail_by_id(data=item)

    async def store(self, data: CreateItemSchema) -> ItemResponseSchema:
        return await self._service.store(data)

    async def update(self, item: ItemModel, data: UpdateItemSchema) -> ItemResponseSchema:
        return await self._service.update(data=data, item=item)

    async def delete(self, data: ItemModel) -> ItemResponseSchema:
        return await self._service.delete(data)
