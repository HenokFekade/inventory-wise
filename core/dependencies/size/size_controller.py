from fastapi import Depends

from apps.size.services.size import SizeService
from apps.size.controllers.size import SizeController
from core.dependencies.size.size_service import size_service_dep


def size_controller_dep(service: SizeService = Depends(size_service_dep)) -> SizeController:
    return SizeController(service)
