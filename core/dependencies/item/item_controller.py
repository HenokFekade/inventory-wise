from fastapi import Depends

from apps.item.services.item import ItemService
from apps.item.controllers.item import ItemController
from core.dependencies.item.item_service import item_service_dep


def item_controller_dep(service: ItemService = Depends(item_service_dep)) -> ItemController:
    return ItemController(service)
