from typing import Optional, List, Tuple
from uuid import UUID

from sqlalchemy import select, func, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from apps.unit.models.unit import UnitModel
from apps.unit.schemas.unit import CreateUnitModelSchema, UpdateUnitModelSchema


class UnitRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    # Optimized query methods
    @staticmethod
    def _base_query():
        return select(UnitModel)

    async def by_pagination(self, search: str, limit: int, offset: int) -> Tuple[List[UnitModel], int]:
        query = self._base_query()

        if search:
            query = query.where(UnitModel.name.ilike(f"%{search}%"))

        query = query.order_by(UnitModel.created_at.desc())  # type: ignore

        result = await self._session.execute(query.limit(limit).offset((offset - 1) * limit))
        results: List[UnitModel] = list(result.scalars().all())
        count_query = select(func.count()).select_from(query.subquery())
        total = await self._session.scalar(count_query)
        return results, total

    async def all(self) -> List[UnitModel]:
        query = self._base_query()
        query = query.order_by(UnitModel.created_at.desc())  # type: ignore
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def by_id(self, _id: UUID) -> Optional[UnitModel]:
        query = self._base_query().where(UnitModel.id == _id)  # type: ignore
        return await self._session.scalar(query)

    async def by_name(self, name: str) -> Optional[UnitModel]:
        query = self._base_query().where(UnitModel.name == name)  # type: ignore
        return await self._session.scalar(query)

    async def store(self, data: CreateUnitModelSchema) -> UnitModel:
        model = UnitModel(**data.model_dump())  # type: ignore
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return model

    async def update(self, _id: UUID, data: UpdateUnitModelSchema) -> Optional[UnitModel]:
        values = data.model_dump(exclude_none=True)
        if not values:
            return None

        query = update(UnitModel).filter(UnitModel.id == _id).values(values)  # type: ignore
        rows_updated = await self._session.execute(query)
        await self._session.commit()

        if rows_updated == 0:
            return None

        return await self.by_id(_id)

    async def delete(self, _id: UUID):
        query = delete(UnitModel).where(UnitModel.id == _id)  # type: ignore
        await self._session.execute(query)
        await self._session.commit()
