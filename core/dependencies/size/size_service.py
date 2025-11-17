from fastapi import Depends

from apps.size.repositories.size import SizeRepository
from apps.size.services.size import SizeService
from core.dependencies.size.size_repo import size_repo_dep


def size_service_dep(repo: SizeRepository = Depends(size_repo_dep)) -> SizeService:
    return SizeService(repo)
