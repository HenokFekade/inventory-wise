from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from apps.item.controllers.item import ItemController
from apps.item.models.item import ItemModel
from apps.item.schemas.item import ItemsResponseSchema, ItemResponseSchema, UpdateItemSchema, \
    CreateItemSchema, ItemFormResponseSchema, ItemDetailResponseSchema
from core.authentications.admin import admin_dep
from core.dependencies import item_controller_dep, item_model_binding, create_item_validator_dep, \
    update_item_validator_dep

item_router = APIRouter(prefix="/items", tags=["Item"])


@item_router.get("", response_model=ItemsResponseSchema)
async def index(
        _=Depends(admin_dep),
        page: int = Query(default=1, ge=1),
        per_page: int = Query(default=10, ge=1, alias="per-page"),
        search: Optional[str] = Query(default=""),
        category_id: Optional[UUID] = Query(default=None),
        color_id: Optional[UUID] = Query(default=None),
        currency_id: Optional[UUID] = Query(default=None),
        size_id: Optional[UUID] = Query(default=None),
        tax_id: Optional[UUID] = Query(default=None),
        unit_id: Optional[UUID] = Query(default=None),
        controller: ItemController = Depends(item_controller_dep),
):
    return await controller.index(
        search=search,
        per_page=per_page,
        page=page,
        category_id=category_id,
        color_id=color_id,
        currency_id=currency_id,
        size_id=size_id,
        tax_id=tax_id,
        unit_id=unit_id,
    )


@item_router.get("/form", response_model=ItemFormResponseSchema)
async def form(
        _=Depends(admin_dep),
        controller: ItemController = Depends(item_controller_dep),
):
    return await controller.form()


@item_router.post("", response_model=ItemResponseSchema, status_code=201)
async def create_item(
        data: CreateItemSchema = Depends(create_item_validator_dep),
        controller: ItemController = Depends(item_controller_dep),
        _=Depends(admin_dep),
):
    return await controller.store(data=data)


@item_router.get("/{id}", response_model=ItemResponseSchema)
async def get_by_id(
        item: ItemModel = Depends(item_model_binding),
        controller: ItemController = Depends(item_controller_dep),
        _=Depends(admin_dep),
):
    return await controller.by_id(item=item)


@item_router.get("/{id}/detail", response_model=ItemDetailResponseSchema)
async def get_detail_by_id(
        item: ItemModel = Depends(item_model_binding),
        controller: ItemController = Depends(item_controller_dep),
        _=Depends(admin_dep),
):
    return await controller.detail_by_id(item=item)


@item_router.patch("/{id}", response_model=ItemResponseSchema)
async def update(
        item: ItemModel = Depends(item_model_binding),
        data: UpdateItemSchema = Depends(update_item_validator_dep),
        controller: ItemController = Depends(item_controller_dep),
        _=Depends(admin_dep),
):
    return await controller.update(item=item, data=data)


@item_router.delete("/{id}", response_model=ItemResponseSchema)
async def update(
        item: ItemModel = Depends(item_model_binding),
        controller: ItemController = Depends(item_controller_dep),
        _=Depends(admin_dep),
):
    return await controller.delete(data=item)
