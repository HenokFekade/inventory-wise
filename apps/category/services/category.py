from typing import Optional

from apps.category.models.category import CategoryModel
from apps.category.repositories.category import CategoryRepository
from apps.category.schemas.category import CategoriesResponseSchema, CategorySchema, CategoryResponseSchema, \
    CreateCategorySchema, CreateCategoryModelSchema, UpdateCategorySchema, UpdateCategoryModelSchema


class CategoryService:
    def __init__(self, repo: CategoryRepository):
        self._repo = repo

    async def index(
            self,
            search: str,
            per_page: int,
            page: int,
            is_publicly_visible: Optional[bool],
            is_active: Optional[bool],
    ) -> CategoriesResponseSchema:
        result, total = await self._repo.by_pagination(
            offset=page,
            search=search,
            limit=per_page,
            is_active=is_active,
            is_publicly_visible=is_publicly_visible,
        )
        data = [CategorySchema.model_validate(value) for value in result]
        return CategoriesResponseSchema(data=data, total=total, page=page, per_page=per_page)

    @staticmethod
    async def by_id(data: CategoryModel) -> CategoryResponseSchema:
        return CategoryResponseSchema(data=CategorySchema.model_validate(data))

    async def store(self, data: CreateCategorySchema) -> CategoryResponseSchema:
        data = await self._repo.store(CreateCategoryModelSchema(**data.model_dump()))
        return CategoryResponseSchema(
            data=CategorySchema.model_validate(data),
            status=201,
            message="Category created successfully",
        )

    async def update(self, category: CategoryModel, data: UpdateCategorySchema) -> CategoryResponseSchema:
        data = UpdateCategoryModelSchema(**data.model_dump())
        result = await self._repo.update(data=data, _id=category.id)
        return CategoryResponseSchema(
            data=CategorySchema.model_validate(result),
            message="Category updated successfully",
        )

    async def delete(self, data: CategoryModel) -> CategoryResponseSchema:
        await self._repo.delete(_id=data.id)
        return CategoryResponseSchema(
            data=CategorySchema.model_validate(data),
            message="Category deleted successfully",
        )
