from fastapi import Depends

from apps.store.services.store import StoreService
from apps.store.controllers.store import StoreController
from core.dependencies.store.store_service import store_service_dep


def store_controller_dep(service: StoreService = Depends(store_service_dep)) -> StoreController:
    return StoreController(service)
