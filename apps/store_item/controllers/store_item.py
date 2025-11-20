from apps.store_item.models.store_item import StoreItemModel
from apps.store_item.schemas.store_item import StoreItemResponseSchema, UpdateStoreItemSchema
from apps.store_item.services.store_item import StoreItemService


class StoreItemController:
    def __init__(self, service: StoreItemService):
        self._service = service

    async def by_id(self, store_item: StoreItemModel) -> StoreItemResponseSchema:
        return await self._service.by_id(data=store_item)

    async def update(self, store_item: StoreItemModel, data: UpdateStoreItemSchema) -> StoreItemResponseSchema:
        return await self._service.update(data=data, store_item=store_item)
