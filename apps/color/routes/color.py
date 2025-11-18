from typing import Optional

from fastapi import APIRouter, Depends, Query

from apps.color.controllers.color import ColorController
from apps.color.models.color import ColorModel
from apps.color.schemas.color import ColorsResponseSchema, ColorResponseSchema, UpdateColorSchema, \
    CreateColorSchema
from core.authentications.admin import admin_dep
from core.dependencies import color_controller_dep, color_model_binding, create_color_validator_dep, \
    update_color_validator_dep

color_router = APIRouter(prefix="/colors", tags=["Color"])


@color_router.get("", response_model=ColorsResponseSchema)
async def index(
        _=Depends(admin_dep),
        page: int = Query(default=1, ge=1),
        per_page: int = Query(default=10, ge=1, alias="per-page"),
        search: Optional[str] = Query(default=""),
        controller: ColorController = Depends(color_controller_dep),
):
    return await controller.index(search=search, per_page=per_page, page=page)


@color_router.post("", response_model=ColorResponseSchema, status_code=201)
async def create_color(
        data: CreateColorSchema = Depends(create_color_validator_dep),
        controller: ColorController = Depends(color_controller_dep),
        _=Depends(admin_dep),
):
    return await controller.store(data=data)


@color_router.get("/{id}", response_model=ColorResponseSchema)
async def get_by_id(
        color: ColorModel = Depends(color_model_binding),
        controller: ColorController = Depends(color_controller_dep),
        _=Depends(admin_dep),
):
    return await controller.by_id(color=color)


@color_router.patch("/{id}", response_model=ColorResponseSchema)
async def update(
        color: ColorModel = Depends(color_model_binding),
        data: UpdateColorSchema = Depends(update_color_validator_dep),
        controller: ColorController = Depends(color_controller_dep),
        _=Depends(admin_dep),
):
    return await controller.update(color=color, data=data)


@color_router.delete("/{id}", response_model=ColorResponseSchema)
async def update(
        color: ColorModel = Depends(color_model_binding),
        controller: ColorController = Depends(color_controller_dep),
        _=Depends(admin_dep),
):
    return await controller.delete(data=color)
