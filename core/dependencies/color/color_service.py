from fastapi import Depends

from apps.color.repositories.color import ColorRepository
from apps.color.services.color import ColorService
from core.dependencies.color.color_repo import color_repo_dep


def color_service_dep(repo: ColorRepository = Depends(color_repo_dep)) -> ColorService:
    return ColorService(repo)
