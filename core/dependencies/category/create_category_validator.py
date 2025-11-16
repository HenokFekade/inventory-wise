from fastapi import Depends

from apps.category.repositories.category import CategoryRepository
from apps.category.schemas.category import CreateCategorySchema
from core.dependencies.category.category_repo import category_repo_dep
from exceptions.unprocessable_entity import UnprocessableEntityException


async def create_category_validator_dep(
        data: CreateCategorySchema,
        repo: CategoryRepository = Depends(category_repo_dep),
) -> CreateCategorySchema:
    if data.category_id:
        result = await repo.by_id(data.category_id)
        if result is None:
            UnprocessableEntityException.throw("category_id", ["Category not found."])
    return data
