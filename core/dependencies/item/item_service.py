from fastapi import Depends

from apps.item.repositories.item import ItemRepository
from apps.item.services.item import ItemService
from core.dependencies.item.item_repo import item_repo_dep


def item_service_dep(repo: ItemRepository = Depends(item_repo_dep)) -> ItemService:
    return ItemService(repo)
