from fastapi import Depends

from apps.store_item.services.store_item import StoreItemService
from apps.store_item.controllers.store_item import StoreItemController
from core.dependencies.store_item.store_item_service import store_item_service_dep


def store_item_controller_dep(service: StoreItemService = Depends(store_item_service_dep)) -> StoreItemController:
    return StoreItemController(service)
