from typing import Optional, List, Tuple
from uuid import UUID

from sqlalchemy import select, func, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from apps.category.models.category import CategoryModel
from apps.category.schemas.category import CreateCategoryModelSchema, UpdateCategoryModelSchema


class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    # Optimized query methods
    @staticmethod
    def _base_query():
        return select(CategoryModel)

    async def by_pagination(
            self,
            search: str,
            limit: int,
            offset: int,
            is_publicly_visible: Optional[bool],
            is_active: Optional[bool],
    ) -> Tuple[List[CategoryModel], int]:
        query = self._base_query()

        if search:
            query = query.where(CategoryModel.name.ilike(f"%{search}%"))

        if is_active is not None:
            query = query.where(CategoryModel.is_active == is_active)  # type: ignore

        if is_publicly_visible is not None:
            query = query.where(CategoryModel.is_publicly_visible == is_publicly_visible)  # type: ignore

        query = query.order_by(CategoryModel.created_at.desc())  # type: ignore

        result = await self._session.execute(query.limit(limit).offset((offset - 1) * limit))
        results: List[CategoryModel] = list(result.scalars().all())
        count_query = select(func.count()).select_from(query.subquery())
        total = await self._session.scalar(count_query)
        return results, total

    async def by_id(self, _id: UUID) -> Optional[CategoryModel]:
        query = self._base_query().where(CategoryModel.id == _id)  # type: ignore
        return await self._session.scalar(query)

    async def store(self, data: CreateCategoryModelSchema) -> CategoryModel:
        model = CategoryModel(**data.model_dump())  # type: ignore
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return model

    async def update(self, _id: UUID, data: UpdateCategoryModelSchema) -> Optional[CategoryModel]:
        values = data.model_dump(exclude_none=True)
        if not values:
            return None

        query = update(CategoryModel).filter(CategoryModel.id == _id).values(values)  # type: ignore
        rows_updated = await self._session.execute(query)
        await self._session.commit()

        if rows_updated == 0:
            return None

        return await self.by_id(_id)

    async def delete(self, _id: UUID):
        query = delete(CategoryModel).where(CategoryModel.id == _id)  # type: ignore
        await self._session.execute(query)
        await self._session.commit()
