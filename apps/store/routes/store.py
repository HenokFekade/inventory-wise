from typing import Optional

from fastapi import APIRouter, Depends, Query

from apps.store.controllers.store import StoreController
from apps.store.models.store import StoreModel
from apps.store.schemas.store import StoresResponseSchema, StoreResponseSchema, UpdateStoreSchema, \
    CreateStoreSchema
from core.authentications.admin import admin_dep
from core.dependencies import store_controller_dep, store_model_binding, create_store_validator_dep, \
    update_store_validator_dep

store_router = APIRouter(prefix="/stores", tags=["Store"])


@store_router.get("", response_model=StoresResponseSchema)
async def index(
        _=Depends(admin_dep),
        page: int = Query(default=1, ge=1),
        per_page: int = Query(default=10, ge=1, alias="per-page"),
        search: Optional[str] = Query(default=""),
        controller: StoreController = Depends(store_controller_dep),
):
    return await controller.index(search=search, per_page=per_page, page=page)


@store_router.post("", response_model=StoreResponseSchema, status_code=201)
async def create_store(
        data: CreateStoreSchema = Depends(create_store_validator_dep),
        controller: StoreController = Depends(store_controller_dep),
        _=Depends(admin_dep),
):
    return await controller.store(data=data)


@store_router.get("/{id}", response_model=StoreResponseSchema)
async def get_by_id(
        store: StoreModel = Depends(store_model_binding),
        controller: StoreController = Depends(store_controller_dep),
        _=Depends(admin_dep),
):
    return await controller.by_id(store=store)


@store_router.patch("/{id}", response_model=StoreResponseSchema)
async def update(
        store: StoreModel = Depends(store_model_binding),
        data: UpdateStoreSchema = Depends(update_store_validator_dep),
        controller: StoreController = Depends(store_controller_dep),
        _=Depends(admin_dep),
):
    return await controller.update(store=store, data=data)


@store_router.delete("/{id}", response_model=StoreResponseSchema)
async def update(
        store: StoreModel = Depends(store_model_binding),
        controller: StoreController = Depends(store_controller_dep),
        _=Depends(admin_dep),
):
    return await controller.delete(data=store)
