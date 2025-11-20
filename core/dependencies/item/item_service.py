from fastapi import Depends

from apps.item.repositories.item import ItemRepository
from apps.item.services.item import ItemService
from apps.store_item.repositories.store_item import StoreItemRepository
from core.dependencies.item.item_repo import item_repo_dep
from core.dependencies.store_item.store_item_repo import store_item_repo_dep


def item_service_dep(
        repo: ItemRepository = Depends(item_repo_dep),
        _store_item_repo: StoreItemRepository = Depends(store_item_repo_dep),
) -> ItemService:
    return ItemService(repo=repo, store_item_repo=_store_item_repo)
