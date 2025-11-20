from fastapi import Depends

from apps.store_item.repositories.store_item import StoreItemRepository
from apps.store_item.services.store_item import StoreItemService
from core.dependencies.store_item.store_item_repo import store_item_repo_dep


def store_item_service_dep(repo: StoreItemRepository = Depends(store_item_repo_dep)) -> StoreItemService:
    return StoreItemService(repo)
