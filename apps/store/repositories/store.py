from typing import Optional, List, Tuple
from uuid import UUID

from sqlalchemy import select, func, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from apps.store.models.store import StoreModel
from apps.store.schemas.store import CreateStoreModelSchema, UpdateStoreModelSchema


class StoreRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    # Optimized query methods
    @staticmethod
    def _base_query():
        return select(StoreModel)

    async def by_pagination(self, search: str, limit: int, offset: int) -> Tuple[List[StoreModel], int]:
        query = self._base_query()
        query = query.order_by(StoreModel.created_at.desc())  # type: ignore

        if search:
            query = query.where(StoreModel.name.ilike(f"%{search}%"))

        result = await self._session.execute(query.limit(limit).offset((offset - 1) * limit))
        results: List[StoreModel] = list(result.scalars().all())
        count_query = select(func.count()).select_from(query.subquery())
        total = await self._session.scalar(count_query)
        return results, total

    async def all(self) -> List[StoreModel]:
        query = self._base_query()
        query = query.order_by(StoreModel.created_at.desc())  # type: ignore
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def by_id(self, _id: UUID) -> Optional[StoreModel]:
        query = self._base_query().where(StoreModel.id == _id)  # type: ignore
        return await self._session.scalar(query)

    async def by_name(self, name: str) -> Optional[StoreModel]:
        query = self._base_query().where(StoreModel.name == name)  # type: ignore
        return await self._session.scalar(query)

    async def store(self, data: CreateStoreModelSchema) -> StoreModel:
        model = StoreModel(**data.model_dump())  # type: ignore
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return model

    async def update(self, _id: UUID, data: UpdateStoreModelSchema) -> Optional[StoreModel]:
        values = data.model_dump(exclude_none=True)
        if not values:
            return None

        query = update(StoreModel).filter(StoreModel.id == _id).values(values)  # type: ignore
        rows_updated = await self._session.execute(query)
        await self._session.commit()

        if rows_updated == 0:
            return None

        return await self.by_id(_id)

    async def delete(self, _id: UUID):
        query = delete(StoreModel).where(StoreModel.id == _id)  # type: ignore
        await self._session.execute(query)
        await self._session.commit()
