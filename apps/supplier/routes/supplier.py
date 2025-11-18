from typing import Optional

from fastapi import APIRouter, Depends, Query

from apps.supplier.controllers.supplier import SupplierController
from apps.supplier.models.supplier import SupplierModel
from apps.supplier.schemas.supplier import SuppliersResponseSchema, SupplierResponseSchema, UpdateSupplierSchema, \
    CreateSupplierSchema
from core.authentications.admin import admin_dep
from core.dependencies import supplier_controller_dep, supplier_model_binding, create_supplier_validator_dep, \
    update_supplier_validator_dep

supplier_router = APIRouter(prefix="/suppliers", tags=["Supplier"])


@supplier_router.get("", response_model=SuppliersResponseSchema)
async def index(
        _=Depends(admin_dep),
        page: int = Query(default=1, ge=1),
        per_page: int = Query(default=10, ge=1, alias="per-page"),
        search: Optional[str] = Query(default=""),
        controller: SupplierController = Depends(supplier_controller_dep),
):
    return await controller.index(search=search, per_page=per_page, page=page)


@supplier_router.post("", response_model=SupplierResponseSchema, status_code=201)
async def create_supplier(
        data: CreateSupplierSchema = Depends(create_supplier_validator_dep),
        controller: SupplierController = Depends(supplier_controller_dep),
        _=Depends(admin_dep),
):
    return await controller.store(data=data)


@supplier_router.get("/{id}", response_model=SupplierResponseSchema)
async def get_by_id(
        supplier: SupplierModel = Depends(supplier_model_binding),
        controller: SupplierController = Depends(supplier_controller_dep),
        _=Depends(admin_dep),
):
    return await controller.by_id(supplier=supplier)


@supplier_router.patch("/{id}", response_model=SupplierResponseSchema)
async def update(
        supplier: SupplierModel = Depends(supplier_model_binding),
        data: UpdateSupplierSchema = Depends(update_supplier_validator_dep),
        controller: SupplierController = Depends(supplier_controller_dep),
        _=Depends(admin_dep),
):
    return await controller.update(supplier=supplier, data=data)


@supplier_router.delete("/{id}", response_model=SupplierResponseSchema)
async def update(
        supplier: SupplierModel = Depends(supplier_model_binding),
        controller: SupplierController = Depends(supplier_controller_dep),
        _=Depends(admin_dep),
):
    return await controller.delete(data=supplier)
