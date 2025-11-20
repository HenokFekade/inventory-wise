from typing import Optional, List
from uuid import UUID

from sqlalchemy import select, func, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from apps.store_item.models.store_item import StoreItemModel
from apps.store_item.schemas.store_item import CreateStoreItemModelSchema, UpdateStoreItemModelSchema


class StoreItemRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    @staticmethod
    def _base_query():
        return select(StoreItemModel)

    async def by_id(self, _id: UUID) -> Optional[StoreItemModel]:
        query = self._base_query().where(StoreItemModel.id == _id)  # type: ignore
        return await self._session.scalar(query)

    async def by_item_store_id(self, item_id: UUID, store_id: UUID) -> Optional[StoreItemModel]:
        query = self._base_query().where(StoreItemModel.store_id == store_id)  # type: ignore
        query = query.where(StoreItemModel.item_id == item_id)  # type: ignore
        query = query.where(StoreItemModel.item_id == item_id)  # type: ignore
        return await self._session.scalar(query)

    async def store(self, data: CreateStoreItemModelSchema) -> StoreItemModel:
        model = StoreItemModel(**data.model_dump())  # type: ignore
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return model

    async def bulk_store(self, data: List[CreateStoreItemModelSchema], commit: bool) -> None:
        models = [StoreItemModel(**value.model_dump()) for value in data]  # type: ignore
        self._session.add_all(models)
        if commit:
            await self._session.commit()
        else:
            await self._session.flush()

    async def update_item_store_id(
            self,
            item_id: UUID,
            store_id: UUID,
            data: UpdateStoreItemModelSchema,
    ) -> Optional[StoreItemModel]:
        values = data.model_dump(exclude_none=True)
        if not values:
            return None

        query = update(StoreItemModel).where(StoreItemModel.store_id == store_id)  # type: ignore
        query = query.where(StoreItemModel.item_id == item_id).values(values)  # type: ignore
        rows_updated = await self._session.execute(query)
        await self._session.commit()

        if rows_updated == 0:
            return None

        return await self.by_item_store_id(item_id=item_id, store_id=store_id)

    async def update_id(self, _id: UUID, data: UpdateStoreItemModelSchema) -> Optional[StoreItemModel]:
        values = data.model_dump(exclude_none=True)
        if not values:
            return None

        query = update(StoreItemModel).where(StoreItemModel.id == _id).values(values)  # type: ignore
        rows_updated = await self._session.execute(query)
        await self._session.commit()

        if rows_updated == 0:
            return None

        return await self.by_id(_id)

    async def delete(self, _id: UUID):
        query = delete(StoreItemModel).where(StoreItemModel.id == _id)  # type: ignore
        await self._session.execute(query)
        await self._session.commit()
