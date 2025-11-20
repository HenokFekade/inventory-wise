from apps.store_item.models.store_item import StoreItemModel
from apps.store_item.repositories.store_item import StoreItemRepository
from apps.store_item.schemas.store_item import StoreItemSchema, StoreItemResponseSchema, \
    CreateStoreItemSchema, CreateStoreItemModelSchema, UpdateStoreItemSchema, UpdateStoreItemModelSchema


class StoreItemService:
    def __init__(self, repo: StoreItemRepository):
        self._repo = repo

    @staticmethod
    async def by_id(data: StoreItemModel) -> StoreItemResponseSchema:
        return StoreItemResponseSchema(data=StoreItemSchema.model_validate(data))

    async def store(self, data: CreateStoreItemSchema) -> StoreItemResponseSchema:
        data = await self._repo.store(CreateStoreItemModelSchema(**data.model_dump()))
        return StoreItemResponseSchema(
            data=StoreItemSchema.model_validate(data),
            status=201,
            message="StoreItem created successfully",
        )

    async def update(self, store_item: StoreItemModel, data: UpdateStoreItemSchema) -> StoreItemResponseSchema:
        data = UpdateStoreItemModelSchema(**data.model_dump())
        result = await self._repo.update_id(data=data, _id=store_item.id)
        return StoreItemResponseSchema(
            data=StoreItemSchema.model_validate(result),
            message="StoreItem updated successfully",
        )
