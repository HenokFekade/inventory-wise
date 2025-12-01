from typing import Optional, List, Tuple
from uuid import UUID

from sqlalchemy import select, func, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from apps.size.models.size import SizeModel
from apps.size.schemas.size import CreateSizeModelSchema, UpdateSizeModelSchema


class SizeRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    # Optimized query methods
    @staticmethod
    def _base_query():
        return select(SizeModel)

    async def by_pagination(self, search: str, limit: int, offset: int) -> Tuple[List[SizeModel], int]:
        query = self._base_query()

        if search:
            query = query.where(SizeModel.name.ilike(f"%{search}%"))

        query = query.order_by(SizeModel.created_at.desc())  # type: ignore

        result = await self._session.execute(query.limit(limit).offset((offset - 1) * limit))
        results: List[SizeModel] = list(result.scalars().all())
        count_query = select(func.count()).select_from(query.subquery())
        total = await self._session.scalar(count_query)
        return results, total

    async def all(self) -> List[SizeModel]:
        query = self._base_query()
        query = query.order_by(SizeModel.created_at.desc())  # type: ignore
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def by_id(self, _id: UUID) -> Optional[SizeModel]:
        query = self._base_query().where(SizeModel.id == _id)  # type: ignore
        return await self._session.scalar(query)

    async def by_name(self, name: str) -> Optional[SizeModel]:
        query = self._base_query().where(SizeModel.name == name)  # type: ignore
        return await self._session.scalar(query)

    async def store(self, data: CreateSizeModelSchema) -> SizeModel:
        model = SizeModel(**data.model_dump())  # type: ignore
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return model

    async def update(self, _id: UUID, data: UpdateSizeModelSchema) -> Optional[SizeModel]:
        values = data.model_dump(exclude_none=True)
        if not values:
            return None

        query = update(SizeModel).filter(SizeModel.id == _id).values(values)  # type: ignore
        rows_updated = await self._session.execute(query)
        await self._session.commit()

        if rows_updated == 0:
            return None

        return await self.by_id(_id)

    async def delete(self, _id: UUID):
        query = delete(SizeModel).where(SizeModel.id == _id)  # type: ignore
        await self._session.execute(query)
        await self._session.commit()
