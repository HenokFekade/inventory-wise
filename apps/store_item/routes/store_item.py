from fastapi import APIRouter, Depends

from apps.store_item.controllers.store_item import StoreItemController
from apps.store_item.models.store_item import StoreItemModel
from apps.store_item.schemas.store_item import StoreItemResponseSchema, UpdateStoreItemSchema
from core.authentications.admin import admin_dep
from core.dependencies import store_item_controller_dep, store_item_model_binding

store_item_router = APIRouter(prefix="/store-items", tags=["Store Item"])


@store_item_router.get("/{id}", response_model=StoreItemResponseSchema)
async def get_by_id(
        store_item: StoreItemModel = Depends(store_item_model_binding),
        controller: StoreItemController = Depends(store_item_controller_dep),
        _=Depends(admin_dep),
):
    return await controller.by_id(store_item=store_item)


@store_item_router.patch("/{id}", response_model=StoreItemResponseSchema)
async def update(
        data: UpdateStoreItemSchema,
        store_item: StoreItemModel = Depends(store_item_model_binding),
        controller: StoreItemController = Depends(store_item_controller_dep),
        _=Depends(admin_dep),
):
    return await controller.update(store_item=store_item, data=data)
