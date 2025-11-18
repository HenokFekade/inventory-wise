from fastapi import Depends

from apps.color.services.color import ColorService
from apps.color.controllers.color import ColorController
from core.dependencies.color.color_service import color_service_dep


def color_controller_dep(service: ColorService = Depends(color_service_dep)) -> ColorController:
    return ColorController(service)
