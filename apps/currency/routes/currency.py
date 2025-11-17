from typing import Optional

from fastapi import APIRouter, Depends, Query

from apps.currency.controllers.currency import CurrencyController
from apps.currency.models.currency import CurrencyModel
from apps.currency.schemas.currency import CurrenciesResponseSchema, CurrencyResponseSchema, UpdateCurrencySchema, \
    CreateCurrencySchema
from core.authentications.admin import admin_dep
from core.dependencies import currency_controller_dep, currency_model_binding, create_currency_validator_dep, \
    update_currency_validator_dep

currency_router = APIRouter(prefix="/currencies", tags=["Currency"])


@currency_router.get("", response_model=CurrenciesResponseSchema)
async def index(
        _=Depends(admin_dep),
        page: int = Query(default=1, ge=1),
        per_page: int = Query(default=10, ge=1, alias="per-page"),
        search: Optional[str] = Query(default=""),
        controller: CurrencyController = Depends(currency_controller_dep),
):
    return await controller.index(search=search, per_page=per_page, page=page)


@currency_router.post("", response_model=CurrencyResponseSchema, status_code=201)
async def create_currency(
        data: CreateCurrencySchema = Depends(create_currency_validator_dep),
        controller: CurrencyController = Depends(currency_controller_dep),
        _=Depends(admin_dep),
):
    return await controller.store(data=data)


@currency_router.get("/{id}", response_model=CurrencyResponseSchema)
async def get_by_id(
        currency: CurrencyModel = Depends(currency_model_binding),
        controller: CurrencyController = Depends(currency_controller_dep),
        _=Depends(admin_dep),
):
    return await controller.by_id(currency=currency)


@currency_router.patch("/{id}", response_model=CurrencyResponseSchema)
async def update(
        currency: CurrencyModel = Depends(currency_model_binding),
        data: UpdateCurrencySchema = Depends(update_currency_validator_dep),
        controller: CurrencyController = Depends(currency_controller_dep),
        _=Depends(admin_dep),
):
    return await controller.update(currency=currency, data=data)


@currency_router.delete("/{id}", response_model=CurrencyResponseSchema)
async def update(
        currency: CurrencyModel = Depends(currency_model_binding),
        controller: CurrencyController = Depends(currency_controller_dep),
        _=Depends(admin_dep),
):
    return await controller.delete(data=currency)
