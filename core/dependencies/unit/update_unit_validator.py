from uuid import UUID

from fastapi import Depends, Path

from apps.unit.repositories.unit import UnitRepository
from apps.unit.schemas.unit import UpdateUnitSchema
from core.dependencies.unit.unit_repo import unit_repo_dep
from exceptions.unprocessable_entity import UnprocessableEntityException


async def update_unit_validator_dep(
        data: UpdateUnitSchema,
        _id: UUID = Path(alias="id"),
        repo: UnitRepository = Depends(unit_repo_dep),
) -> UpdateUnitSchema:
    result = await repo.by_name(data.name)
    if result and result.id != _id:
        UnprocessableEntityException.throw("name", ["Name already taken."])
    return data
