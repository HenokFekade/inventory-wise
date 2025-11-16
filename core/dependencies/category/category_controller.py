from fastapi import Depends

from apps.category.services.category import CategoryService
from apps.category.controllers.category import CategoryController
from core.dependencies.category.category_service import category_service_dep


def category_controller_dep(service: CategoryService = Depends(category_service_dep)) -> CategoryController:
    return CategoryController(service)
