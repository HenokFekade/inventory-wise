from typing import Optional

from fastapi import APIRouter, Depends, Query

from apps.size.controllers.size import SizeController
from apps.size.models.size import SizeModel
from apps.size.schemas.size import SizesResponseSchema, SizeResponseSchema, UpdateSizeSchema, \
    CreateSizeSchema
from core.authentications.admin import admin_dep
from core.dependencies import size_controller_dep, size_model_binding, create_size_validator_dep, \
    update_size_validator_dep

size_router = APIRouter(prefix="/sizes", tags=["Size"])


@size_router.get("", response_model=SizesResponseSchema)
async def index(
        _=Depends(admin_dep),
        page: int = Query(default=1, ge=1),
        per_page: int = Query(default=10, ge=1, alias="per-page"),
        search: Optional[str] = Query(default=""),
        controller: SizeController = Depends(size_controller_dep),
):
    return await controller.index(search=search, per_page=per_page, page=page)


@size_router.post("", response_model=SizeResponseSchema, status_code=201)
async def create_size(
        data: CreateSizeSchema = Depends(create_size_validator_dep),
        controller: SizeController = Depends(size_controller_dep),
        _=Depends(admin_dep),
):
    return await controller.store(data=data)


@size_router.get("/{id}", response_model=SizeResponseSchema)
async def get_by_id(
        size: SizeModel = Depends(size_model_binding),
        controller: SizeController = Depends(size_controller_dep),
        _=Depends(admin_dep),
):
    return await controller.by_id(size=size)


@size_router.patch("/{id}", response_model=SizeResponseSchema)
async def update(
        size: SizeModel = Depends(size_model_binding),
        data: UpdateSizeSchema = Depends(update_size_validator_dep),
        controller: SizeController = Depends(size_controller_dep),
        _=Depends(admin_dep),
):
    return await controller.update(size=size, data=data)


@size_router.delete("/{id}", response_model=SizeResponseSchema)
async def update(
        size: SizeModel = Depends(size_model_binding),
        controller: SizeController = Depends(size_controller_dep),
        _=Depends(admin_dep),
):
    return await controller.delete(data=size)
