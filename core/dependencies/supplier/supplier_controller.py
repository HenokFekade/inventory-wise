from fastapi import Depends

from apps.supplier.services.supplier import SupplierService
from apps.supplier.controllers.supplier import SupplierController
from core.dependencies.supplier.supplier_service import supplier_service_dep


def supplier_controller_dep(service: SupplierService = Depends(supplier_service_dep)) -> SupplierController:
    return SupplierController(service)
