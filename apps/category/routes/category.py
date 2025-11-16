from typing import Optional

from fastapi import APIRouter, Depends, Query

from apps.category.controllers.category import CategoryController
from apps.category.models.category import CategoryModel
from apps.category.schemas.category import CategoriesResponseSchema, CategoryResponseSchema, UpdateCategorySchema, \
    CreateCategorySchema
from core.authentications.admin import admin_dep
from core.dependencies import category_controller_dep, category_model_binding, create_category_validator_dep, \
    update_category_validator_dep

category_router = APIRouter(prefix="/categories", tags=["Category"])


@category_router.get("", response_model=CategoriesResponseSchema)
async def index(
        _=Depends(admin_dep),
        page: int = Query(default=1, ge=1),
        per_page: int = Query(default=10, ge=1, alias="per-page"),
        search: Optional[str] = Query(default=""),
        is_active: Optional[bool] = Query(default=None),
        is_publicly_visible: Optional[bool] = Query(default=None),
        controller: CategoryController = Depends(category_controller_dep),
):
    return await controller.index(
        search=search,
        per_page=per_page,
        page=page,
        is_publicly_visible=is_publicly_visible,
        is_active=is_active,
    )


@category_router.post("", response_model=CategoryResponseSchema, status_code=201)
async def create_category(
        data: CreateCategorySchema = Depends(create_category_validator_dep),
        controller: CategoryController = Depends(category_controller_dep),
        _=Depends(admin_dep),
):
    return await controller.store(data=data)


@category_router.get("/{id}", response_model=CategoryResponseSchema)
async def get_by_id(
        category: CategoryModel = Depends(category_model_binding),
        controller: CategoryController = Depends(category_controller_dep),
        _=Depends(admin_dep),
):
    return await controller.by_id(category=category)


@category_router.patch("/{id}", response_model=CategoryResponseSchema)
async def update(
        category: CategoryModel = Depends(category_model_binding),
        data: UpdateCategorySchema = Depends(update_category_validator_dep),
        controller: CategoryController = Depends(category_controller_dep),
        _=Depends(admin_dep),
):
    return await controller.update(category=category, data=data)


@category_router.delete("/{id}", response_model=CategoryResponseSchema)
async def update(
        category: CategoryModel = Depends(category_model_binding),
        controller: CategoryController = Depends(category_controller_dep),
        _=Depends(admin_dep),
):
    return await controller.delete(data=category)
