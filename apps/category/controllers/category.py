from typing import Optional

from apps.category.models.category import CategoryModel
from apps.category.schemas.category import CategoriesResponseSchema, CategoryResponseSchema, CreateCategorySchema, \
    UpdateCategorySchema
from apps.category.services.category import CategoryService


class CategoryController:
    def __init__(self, service: CategoryService):
        self._service = service

    async def index(
            self,
            search: str,
            per_page: int,
            page: int,
            is_publicly_visible: Optional[bool],
            is_active: Optional[bool],
    ) -> CategoriesResponseSchema:
        return await self._service.index(
            search=search,
            per_page=per_page,
            page=page,
            is_active=is_active,
            is_publicly_visible=is_publicly_visible,
        )

    async def by_id(self, category: CategoryModel) -> CategoryResponseSchema:
        return await self._service.by_id(data=category)

    async def store(self, data: CreateCategorySchema) -> CategoryResponseSchema:
        return await self._service.store(data)

    async def update(self, category: CategoryModel, data: UpdateCategorySchema) -> CategoryResponseSchema:
        return await self._service.update(data=data, category=category)

    async def delete(self, data: CategoryModel) -> CategoryResponseSchema:
        return await self._service.delete(data)
