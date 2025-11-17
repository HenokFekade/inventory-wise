from fastapi import Depends

from apps.unit.repositories.unit import UnitRepository
from apps.unit.services.unit import UnitService
from core.dependencies.unit.unit_repo import unit_repo_dep


def unit_service_dep(repo: UnitRepository = Depends(unit_repo_dep)) -> UnitService:
    return UnitService(repo)
