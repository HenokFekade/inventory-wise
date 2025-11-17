from apps.unit.models.unit import UnitModel
from apps.unit.schemas.unit import UnitsResponseSchema, UnitResponseSchema, CreateUnitSchema, \
    UpdateUnitSchema
from apps.unit.services.unit import UnitService


class UnitController:
    def __init__(self, service: UnitService):
        self._service = service

    async def index(self, search: str, per_page: int, page: int) -> UnitsResponseSchema:
        return await self._service.index(search=search, per_page=per_page, page=page)

    async def by_id(self, unit: UnitModel) -> UnitResponseSchema:
        return await self._service.by_id(data=unit)

    async def store(self, data: CreateUnitSchema) -> UnitResponseSchema:
        return await self._service.store(data)

    async def update(self, unit: UnitModel, data: UpdateUnitSchema) -> UnitResponseSchema:
        return await self._service.update(data=data, unit=unit)

    async def delete(self, data: UnitModel) -> UnitResponseSchema:
        return await self._service.delete(data)
