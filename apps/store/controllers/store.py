from apps.store.models.store import StoreModel
from apps.store.schemas.store import StoresResponseSchema, StoreResponseSchema, CreateStoreSchema, \
    UpdateStoreSchema
from apps.store.services.store import StoreService


class StoreController:
    def __init__(self, service: StoreService):
        self._service = service

    async def index(self, search: str, per_page: int, page: int) -> StoresResponseSchema:
        return await self._service.index(search=search, per_page=per_page, page=page)

    async def by_id(self, store: StoreModel) -> StoreResponseSchema:
        return await self._service.by_id(data=store)

    async def store(self, data: CreateStoreSchema) -> StoreResponseSchema:
        return await self._service.store(data)

    async def update(self, store: StoreModel, data: UpdateStoreSchema) -> StoreResponseSchema:
        return await self._service.update(data=data, store=store)

    async def delete(self, data: StoreModel) -> StoreResponseSchema:
        return await self._service.delete(data)
