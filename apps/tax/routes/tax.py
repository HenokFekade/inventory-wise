from typing import Optional

from fastapi import APIRouter, Depends, Query

from apps.tax.controllers.tax import TaxController
from apps.tax.models.tax import TaxModel
from apps.tax.schemas.tax import TaxsResponseSchema, TaxResponseSchema, UpdateTaxSchema, \
    CreateTaxSchema
from core.authentications.admin import admin_dep
from core.dependencies import tax_controller_dep, tax_model_binding, create_tax_validator_dep, update_tax_validator_dep

tax_router = APIRouter(prefix="/taxes", tags=["Tax"])


@tax_router.get("", response_model=TaxsResponseSchema)
async def index(
        _=Depends(admin_dep),
        page: int = Query(default=1, ge=1),
        per_page: int = Query(default=10, ge=1, alias="per-page"),
        search: Optional[str] = Query(default=""),
        controller: TaxController = Depends(tax_controller_dep),
):
    return await controller.index(search=search, per_page=per_page, page=page)


@tax_router.post("", response_model=TaxResponseSchema, status_code=201)
async def create_tax(
        data: CreateTaxSchema = Depends(create_tax_validator_dep),
        controller: TaxController = Depends(tax_controller_dep),
        _=Depends(admin_dep),
):
    return await controller.store(data=data)


@tax_router.get("/{id}", response_model=TaxResponseSchema)
async def get_by_id(
        tax: TaxModel = Depends(tax_model_binding),
        controller: TaxController = Depends(tax_controller_dep),
        _=Depends(admin_dep),
):
    return await controller.by_id(tax=tax)


@tax_router.patch("/{id}", response_model=TaxResponseSchema)
async def update(
        tax: TaxModel = Depends(tax_model_binding),
        data: UpdateTaxSchema = Depends(update_tax_validator_dep),
        controller: TaxController = Depends(tax_controller_dep),
        _=Depends(admin_dep),
):
    return await controller.update(tax=tax, data=data)


@tax_router.delete("/{id}", response_model=TaxResponseSchema)
async def update(
        tax: TaxModel = Depends(tax_model_binding),
        controller: TaxController = Depends(tax_controller_dep),
        _=Depends(admin_dep),
):
    return await controller.delete(data=tax)
