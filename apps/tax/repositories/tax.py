from typing import Optional, List, Tuple
from uuid import UUID

from sqlalchemy import select, func, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from apps.tax.models.tax import TaxModel
from apps.tax.schemas.tax import CreateTaxModelSchema, UpdateTaxModelSchema


class TaxRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    # Optimized query methods
    @staticmethod
    def _base_query():
        return select(TaxModel)

    async def by_pagination(self, search: str, limit: int, offset: int) -> Tuple[List[TaxModel], int]:
        query = self._base_query()
        query = query.order_by(TaxModel.created_at.desc())  # type: ignore

        result = await self._session.execute(query.limit(limit).offset((offset - 1) * limit))
        results: List[TaxModel] = list(result.scalars().all())
        count_query = select(func.count()).select_from(query.subquery())
        total = await self._session.scalar(count_query)
        return results, total

    async def by_id(self, _id: UUID) -> Optional[TaxModel]:
        query = self._base_query().where(TaxModel.id == _id)  # type: ignore
        return await self._session.scalar(query)

    async def by_percent(self, percent: int) -> Optional[TaxModel]:
        query = self._base_query().where(TaxModel.percent == percent)  # type: ignore
        return await self._session.scalar(query)

    async def store(self, data: CreateTaxModelSchema) -> TaxModel:
        model = TaxModel(**data.model_dump())  # type: ignore
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return model

    async def update(self, _id: UUID, data: UpdateTaxModelSchema) -> Optional[TaxModel]:
        values = data.model_dump(exclude_none=True)
        if not values:
            return None

        query = update(TaxModel).filter(TaxModel.id == _id).values(values)  # type: ignore
        rows_updated = await self._session.execute(query)
        await self._session.commit()

        if rows_updated == 0:
            return None

        return await self.by_id(_id)

    async def delete(self, _id: UUID):
        query = delete(TaxModel).where(TaxModel.id == _id)  # type: ignore
        await self._session.execute(query)
        await self._session.commit()
