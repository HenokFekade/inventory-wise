from fastapi import Depends

from apps.unit.services.unit import UnitService
from apps.unit.controllers.unit import UnitController
from core.dependencies.unit.unit_service import unit_service_dep


def unit_controller_dep(service: UnitService = Depends(unit_service_dep)) -> UnitController:
    return UnitController(service)
