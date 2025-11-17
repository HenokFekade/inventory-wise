from apps.store.models.store import StoreModel
from apps.store.repositories.store import StoreRepository
from apps.store.schemas.store import StoresResponseSchema, StoreSchema, StoreResponseSchema, \
    CreateStoreSchema, CreateStoreModelSchema, UpdateStoreSchema, UpdateStoreModelSchema


class StoreService:
    def __init__(self, repo: StoreRepository):
        self._repo = repo

    async def index(self, search: str, per_page: int, page: int) -> StoresResponseSchema:
        result, total = await self._repo.by_pagination(offset=page, search=search, limit=per_page)
        data = [StoreSchema.model_validate(value) for value in result]
        return StoresResponseSchema(data=data, total=total, page=page, per_page=per_page)

    @staticmethod
    async def by_id(data: StoreModel) -> StoreResponseSchema:
        return StoreResponseSchema(data=StoreSchema.model_validate(data))

    async def store(self, data: CreateStoreSchema) -> StoreResponseSchema:
        data = await self._repo.store(CreateStoreModelSchema(**data.model_dump()))
        return StoreResponseSchema(
            data=StoreSchema.model_validate(data),
            status=201,
            message="Store created successfully",
        )

    async def update(self, store: StoreModel, data: UpdateStoreSchema) -> StoreResponseSchema:
        data = UpdateStoreModelSchema(**data.model_dump())
        result = await self._repo.update(data=data, _id=store.id)
        return StoreResponseSchema(
            data=StoreSchema.model_validate(result),
            message="Store updated successfully",
        )

    async def delete(self, data: StoreModel) -> StoreResponseSchema:
        await self._repo.delete(_id=data.id)
        return StoreResponseSchema(
            data=StoreSchema.model_validate(data),
            message="Store deleted successfully",
        )
