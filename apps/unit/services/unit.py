from apps.unit.models.unit import UnitModel
from apps.unit.repositories.unit import UnitRepository
from apps.unit.schemas.unit import UnitsResponseSchema, UnitSchema, UnitResponseSchema, \
    CreateUnitSchema, CreateUnitModelSchema, UpdateUnitSchema, UpdateUnitModelSchema


class UnitService:
    def __init__(self, repo: UnitRepository):
        self._repo = repo

    async def index(self, search: str, per_page: int, page: int) -> UnitsResponseSchema:
        result, total = await self._repo.by_pagination(offset=page, search=search, limit=per_page)
        data = [UnitSchema.model_validate(value) for value in result]
        return UnitsResponseSchema(data=data, total=total, page=page, per_page=per_page)

    @staticmethod
    async def by_id(data: UnitModel) -> UnitResponseSchema:
        return UnitResponseSchema(data=UnitSchema.model_validate(data))

    async def store(self, data: CreateUnitSchema) -> UnitResponseSchema:
        data = await self._repo.store(CreateUnitModelSchema(**data.model_dump()))
        return UnitResponseSchema(
            data=UnitSchema.model_validate(data),
            status=201,
            message="Unit created successfully",
        )

    async def update(self, unit: UnitModel, data: UpdateUnitSchema) -> UnitResponseSchema:
        data = UpdateUnitModelSchema(**data.model_dump())
        result = await self._repo.update(data=data, _id=unit.id)
        return UnitResponseSchema(
            data=UnitSchema.model_validate(result),
            message="Unit updated successfully",
        )

    async def delete(self, data: UnitModel) -> UnitResponseSchema:
        await self._repo.delete(_id=data.id)
        return UnitResponseSchema(
            data=UnitSchema.model_validate(data),
            message="Unit deleted successfully",
        )
