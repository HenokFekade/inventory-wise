from typing import Optional, List, Tuple
from uuid import UUID

from sqlalchemy import select, func, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from apps.item.models.item import ItemModel
from apps.item.schemas.item import CreateItemModelSchema, UpdateItemModelSchema


class ItemRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    # Optimized query methods
    @staticmethod
    def _base_query():
        return select(ItemModel)

    async def by_pagination(self, search: str, limit: int, offset: int) -> Tuple[List[ItemModel], int]:
        query = self._base_query()
        query = query.order_by(ItemModel.created_at.desc())  # type: ignore

        result = await self._session.execute(query.limit(limit).offset((offset - 1) * limit))
        results: List[ItemModel] = list(result.scalars().all())
        count_query = select(func.count()).select_from(query.subquery())
        total = await self._session.scalar(count_query)
        return results, total

    async def by_id(self, _id: UUID) -> Optional[ItemModel]:
        query = self._base_query().where(ItemModel.id == _id)  # type: ignore
        return await self._session.scalar(query)

    async def store(self, data: CreateItemModelSchema) -> ItemModel:
        model = ItemModel(**data.model_dump())  # type: ignore
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return model

    async def update(self, _id: UUID, data: UpdateItemModelSchema) -> Optional[ItemModel]:
        values = data.model_dump(exclude_none=True)
        if not values:
            return None

        query = update(ItemModel).filter(ItemModel.id == _id).values(values)  # type: ignore
        rows_updated = await self._session.execute(query)
        await self._session.commit()

        if rows_updated == 0:
            return None

        return await self.by_id(_id)

    async def delete(self, _id: UUID):
        query = delete(ItemModel).where(ItemModel.id == _id)  # type: ignore
        await self._session.execute(query)
        await self._session.commit()
