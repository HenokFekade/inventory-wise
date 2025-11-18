from apps.item.models.item import ItemModel
from apps.item.repositories.item import ItemRepository
from apps.item.schemas.item import ItemsResponseSchema, ItemSchema, ItemResponseSchema, \
    CreateItemSchema, CreateItemModelSchema, UpdateItemSchema, UpdateItemModelSchema


class ItemService:
    def __init__(self, repo: ItemRepository):
        self._repo = repo

    async def index(self, search: str, per_page: int, page: int) -> ItemsResponseSchema:
        result, total = await self._repo.by_pagination(offset=page, search=search, limit=per_page)
        data = [ItemSchema.model_validate(value) for value in result]
        return ItemsResponseSchema(data=data, total=total, page=page, per_page=per_page)

    @staticmethod
    async def by_id(data: ItemModel) -> ItemResponseSchema:
        return ItemResponseSchema(data=ItemSchema.model_validate(data))

    async def store(self, data: CreateItemSchema) -> ItemResponseSchema:
        data = await self._repo.store(CreateItemModelSchema(**data.model_dump()))
        return ItemResponseSchema(
            data=ItemSchema.model_validate(data),
            status=201,
            message="Item created successfully",
        )

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
