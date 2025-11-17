from typing import Optional, List, Tuple
from uuid import UUID

from sqlalchemy import select, func, delete, update, or_
from sqlalchemy.ext.asyncio import AsyncSession

from apps.customer.models.customer import CustomerModel
from apps.customer.schemas.customer import CreateCustomerModelSchema, UpdateCustomerModelSchema


class CustomerRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    # Optimized query methods
    @staticmethod
    def _base_query():
        return select(CustomerModel)

    async def by_pagination(self, search: str, limit: int, offset: int) -> Tuple[List[CustomerModel], int]:
        query = self._base_query()
        query = query.order_by(CustomerModel.created_at.desc())  # type: ignore

        if search:
            query = query.where(
                or_(
                    CustomerModel.name.ilike(f"%{search}%"),
                    CustomerModel.phone.ilike(f"%{search}%"),
                    CustomerModel.additional_phone.ilike(f"%{search}%"),
                )
            )
        result = await self._session.execute(query.limit(limit).offset((offset - 1) * limit))
        results: List[CustomerModel] = list(result.scalars().all())
        count_query = select(func.count()).select_from(query.subquery())
        total = await self._session.scalar(count_query)
        return results, total

    async def by_id(self, _id: UUID) -> Optional[CustomerModel]:
        query = self._base_query().where(CustomerModel.id == _id)  # type: ignore
        return await self._session.scalar(query)

    async def by_phone(self, phone: str) -> Optional[CustomerModel]:
        query = self._base_query().where(CustomerModel.phone == phone)  # type: ignore
        return await self._session.scalar(query)

    async def store(self, data: CreateCustomerModelSchema) -> CustomerModel:
        model = CustomerModel(**data.model_dump())  # type: ignore
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return model

    async def update(self, _id: UUID, data: UpdateCustomerModelSchema) -> Optional[CustomerModel]:
        values = data.model_dump(exclude_none=True)
        if not values:
            return None

        query = update(CustomerModel).filter(CustomerModel.id == _id).values(values)  # type: ignore
        rows_updated = await self._session.execute(query)
        await self._session.commit()

        if rows_updated == 0:
            return None

        return await self.by_id(_id)

    async def delete(self, _id: UUID):
        query = delete(CustomerModel).where(CustomerModel.id == _id)  # type: ignore
        await self._session.execute(query)
        await self._session.commit()
