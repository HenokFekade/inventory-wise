from fastapi import Depends

from apps.category.repositories.category import CategoryRepository
from apps.category.services.category import CategoryService
from core.dependencies.category.category_repo import category_repo_dep


def category_service_dep(repo: CategoryRepository = Depends(category_repo_dep)) -> CategoryService:
    return CategoryService(repo)
