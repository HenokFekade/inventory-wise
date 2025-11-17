from fastapi import Depends

from apps.store.repositories.store import StoreRepository
from apps.store.services.store import StoreService
from core.dependencies.store.store_repo import store_repo_dep


def store_service_dep(repo: StoreRepository = Depends(store_repo_dep)) -> StoreService:
    return StoreService(repo)
