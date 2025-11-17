from typing import Optional, List, Tuple
from uuid import UUID

from sqlalchemy import select, func, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from apps.currency.models.currency import CurrencyModel
from apps.currency.schemas.currency import CreateCurrencyModelSchema, UpdateCurrencyModelSchema


class CurrencyRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    # Optimized query methods
    @staticmethod
    def _base_query():
        return select(CurrencyModel)

    async def by_pagination(self, search: str, limit: int, offset: int) -> Tuple[List[CurrencyModel], int]:
        query = self._base_query()
        query = query.order_by(CurrencyModel.created_at.desc())  # type: ignore

        result = await self._session.execute(query.limit(limit).offset((offset - 1) * limit))
        results: List[CurrencyModel] = list(result.scalars().all())
        count_query = select(func.count()).select_from(query.subquery())
        total = await self._session.scalar(count_query)
        return results, total

    async def by_id(self, _id: UUID) -> Optional[CurrencyModel]:
        query = self._base_query().where(CurrencyModel.id == _id)  # type: ignore
        return await self._session.scalar(query)

    async def by_code(self, code: str) -> Optional[CurrencyModel]:
        query = self._base_query().where(CurrencyModel.code == code)  # type: ignore
        return await self._session.scalar(query)

    async def by_name(self, name: str) -> Optional[CurrencyModel]:
        query = self._base_query().where(CurrencyModel.name == name)  # type: ignore
        return await self._session.scalar(query)

    async def store(self, data: CreateCurrencyModelSchema) -> CurrencyModel:
        model = CurrencyModel(**data.model_dump())  # type: ignore
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return model

    async def update(self, _id: UUID, data: UpdateCurrencyModelSchema) -> Optional[CurrencyModel]:
        values = data.model_dump(exclude_none=True)
        if not values:
            return None

        query = update(CurrencyModel).filter(CurrencyModel.id == _id).values(values)  # type: ignore
        rows_updated = await self._session.execute(query)
        await self._session.commit()

        if rows_updated == 0:
            return None

        return await self.by_id(_id)

    async def delete(self, _id: UUID):
        query = delete(CurrencyModel).where(CurrencyModel.id == _id)  # type: ignore
        await self._session.execute(query)
        await self._session.commit()
