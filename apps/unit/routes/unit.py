from typing import Optional

from fastapi import APIRouter, Depends, Query

from apps.unit.controllers.unit import UnitController
from apps.unit.models.unit import UnitModel
from apps.unit.schemas.unit import UnitsResponseSchema, UnitResponseSchema, UpdateUnitSchema, \
    CreateUnitSchema
from core.authentications.admin import admin_dep
from core.dependencies import unit_controller_dep, unit_model_binding, create_unit_validator_dep, \
    update_unit_validator_dep

unit_router = APIRouter(prefix="/units", tags=["Unit"])


@unit_router.get("", response_model=UnitsResponseSchema)
async def index(
        _=Depends(admin_dep),
        page: int = Query(default=1, ge=1),
        per_page: int = Query(default=10, ge=1, alias="per-page"),
        search: Optional[str] = Query(default=""),
        controller: UnitController = Depends(unit_controller_dep),
):
    return await controller.index(search=search, per_page=per_page, page=page)


@unit_router.post("", response_model=UnitResponseSchema, status_code=201)
async def create_unit(
        data: CreateUnitSchema = Depends(create_unit_validator_dep),
        controller: UnitController = Depends(unit_controller_dep),
        _=Depends(admin_dep),
):
    return await controller.store(data=data)


@unit_router.get("/{id}", response_model=UnitResponseSchema)
async def get_by_id(
        unit: UnitModel = Depends(unit_model_binding),
        controller: UnitController = Depends(unit_controller_dep),
        _=Depends(admin_dep),
):
    return await controller.by_id(unit=unit)


@unit_router.patch("/{id}", response_model=UnitResponseSchema)
async def update(
        unit: UnitModel = Depends(unit_model_binding),
        data: UpdateUnitSchema = Depends(update_unit_validator_dep),
        controller: UnitController = Depends(unit_controller_dep),
        _=Depends(admin_dep),
):
    return await controller.update(unit=unit, data=data)


@unit_router.delete("/{id}", response_model=UnitResponseSchema)
async def update(
        unit: UnitModel = Depends(unit_model_binding),
        controller: UnitController = Depends(unit_controller_dep),
        _=Depends(admin_dep),
):
    return await controller.delete(data=unit)
