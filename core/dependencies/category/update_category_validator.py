from fastapi import Depends

from apps.category.repositories.category import CategoryRepository
from apps.category.schemas.category import UpdateCategorySchema
from core.dependencies.category.category_repo import category_repo_dep
from exceptions.unprocessable_entity import UnprocessableEntityException


async def update_category_validator_dep(
        data: UpdateCategorySchema,
        repo: CategoryRepository = Depends(category_repo_dep),
) -> UpdateCategorySchema:
    if data.category_id:
        result = await repo.by_id(data.category_id)
        if result is None:
            UnprocessableEntityException.throw("category_id", ["Category not found."])
    return data
