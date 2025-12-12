from typing import Optional, List, Tuple
from uuid import UUID

from sqlalchemy import select, func, delete, update, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from apps.item.models.item import ItemModel
from apps.item.schemas.item import CreateItemModelSchema, UpdateItemModelSchema
from apps.store_item.models.store_item import StoreItemModel


class ItemRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    # Optimized query methods
    @staticmethod
    def _base_query():
        return select(ItemModel)

    async def by_pagination(
            self,
            search: str,
            limit: int,
            offset: int,
            category_id: Optional[UUID],
            color_id: Optional[UUID],
            currency_id: Optional[UUID],
            size_id: Optional[UUID],
            tax_id: Optional[UUID],
            unit_id: Optional[UUID],
    ) -> Tuple[List[ItemModel], int]:
        query = self._base_query()

        if search:
            query = query.where(
                or_(
                    ItemModel.name.ilike(f"%{search}%"),
                    ItemModel.code.ilike(f"%{search}%"),
                    ItemModel.description.ilike(f"%{search}%"),
                )
            )
        if category_id:
            query = query.where(ItemModel.category_id ==category_id) # type: ignore
        if currency_id:
            query = query.where(ItemModel.currency_id ==currency_id) # type: ignore
        if color_id:
            query = query.where(ItemModel.color_id ==color_id) # type: ignore
        if currency_id:
            query = query.where(ItemModel.currency_id ==currency_id) # type: ignore
        if size_id:
            query = query.where(ItemModel.size_id ==size_id) # type: ignore
        if tax_id:
            query = query.where(ItemModel.tax_id ==tax_id) # type: ignore
        if unit_id:
            query = query.where(ItemModel.unit_id ==unit_id) # type: ignore

        query = query.order_by(ItemModel.created_at.desc())  # type: ignore

        count_query = select(func.count()).select_from(query.subquery())
        total = await self._session.scalar(count_query)
        query = query.options(joinedload(ItemModel.category), joinedload(ItemModel.color), joinedload(ItemModel.size))
        query = query.options( joinedload(ItemModel.currency), joinedload(ItemModel.unit), joinedload(ItemModel.tax))
        result = await self._session.execute(query.limit(limit).offset((offset - 1) * limit))
        results: List[ItemModel] = list(result.scalars().all())
        return results, total

    async def by_id_with_all_relation_except_store(self, _id: UUID) -> Optional[ItemModel]:
        query = self._base_query().where(ItemModel.id == _id)  # type: ignore
        query = query.options(joinedload(ItemModel.category), joinedload(ItemModel.color), joinedload(ItemModel.size))
        query = query.options(joinedload(ItemModel.currency), joinedload(ItemModel.unit), joinedload(ItemModel.tax))
        return await self._session.scalar(query)

    async def by_id_with_all_relation(self, _id: UUID) -> Optional[ItemModel]:
        query = self._base_query().where(ItemModel.id == _id)  # type: ignore
        query = query.options(joinedload(ItemModel.category), joinedload(ItemModel.color), joinedload(ItemModel.size))
        query = query.options(joinedload(ItemModel.currency), joinedload(ItemModel.unit), joinedload(ItemModel.tax))
        query = query.options(joinedload(ItemModel.store_items).joinedload(StoreItemModel.store))
        return await self._session.scalar(query)

    async def by_id(self, _id: UUID) -> Optional[ItemModel]:
        query = self._base_query().where(ItemModel.id == _id)  # type: ignore
        return await self._session.scalar(query)

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()

    async def store(self, data: CreateItemModelSchema, commit: bool) -> ItemModel:
        model = ItemModel(**data.model_dump(mode="json"))  # type: ignore
        self._session.add(model)
        if commit:
            await self._session.commit()
        else:
            await self._session.flush()
        await self._session.refresh(model)
        return model

    async def update(self, _id: UUID, data: UpdateItemModelSchema) -> Optional[ItemModel]:
        values = data.model_dump(exclude_none=True, mode="json")
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
