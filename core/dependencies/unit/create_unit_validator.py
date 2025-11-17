from fastapi import Depends

from apps.unit.repositories.unit import UnitRepository
from apps.unit.schemas.unit import CreateUnitSchema
from core.dependencies.unit.unit_repo import unit_repo_dep
from exceptions.unprocessable_entity import UnprocessableEntityException


async def create_unit_validator_dep(
        data: CreateUnitSchema,
        repo: UnitRepository = Depends(unit_repo_dep),
) -> CreateUnitSchema:
    result = await repo.by_name(data.name)
    if result:
        UnprocessableEntityException.throw("name", ["Name already taken."])
    return data
