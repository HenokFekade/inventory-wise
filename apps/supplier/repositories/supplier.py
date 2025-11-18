from typing import Optional, List, Tuple
from uuid import UUID

from sqlalchemy import select, func, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from apps.supplier.models.supplier import SupplierModel
from apps.supplier.schemas.supplier import CreateSupplierModelSchema, UpdateSupplierModelSchema


class SupplierRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    # Optimized query methods
    @staticmethod
    def _base_query():
        return select(SupplierModel)

    async def by_pagination(self, search: str, limit: int, offset: int) -> Tuple[List[SupplierModel], int]:
        query = self._base_query()
        query = query.order_by(SupplierModel.created_at.desc())  # type: ignore

        result = await self._session.execute(query.limit(limit).offset((offset - 1) * limit))
        results: List[SupplierModel] = list(result.scalars().all())
        count_query = select(func.count()).select_from(query.subquery())
        total = await self._session.scalar(count_query)
        return results, total

    async def by_id(self, _id: UUID) -> Optional[SupplierModel]:
        query = self._base_query().where(SupplierModel.id == _id)  # type: ignore
        return await self._session.scalar(query)

    async def by_phone(self, phone: str) -> Optional[SupplierModel]:
        query = self._base_query().where(SupplierModel.phone == phone)  # type: ignore
        return await self._session.scalar(query)

    async def store(self, data: CreateSupplierModelSchema) -> SupplierModel:
        model = SupplierModel(**data.model_dump())  # type: ignore
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return model

    async def update(self, _id: UUID, data: UpdateSupplierModelSchema) -> Optional[SupplierModel]:
        values = data.model_dump(exclude_none=True)
        if not values:
            return None

        query = update(SupplierModel).filter(SupplierModel.id == _id).values(values)  # type: ignore
        rows_updated = await self._session.execute(query)
        await self._session.commit()

        if rows_updated == 0:
            return None

        return await self.by_id(_id)

    async def delete(self, _id: UUID):
        query = delete(SupplierModel).where(SupplierModel.id == _id)  # type: ignore
        await self._session.execute(query)
        await self._session.commit()
