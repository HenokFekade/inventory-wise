from fastapi import Depends

from apps.supplier.repositories.supplier import SupplierRepository
from apps.supplier.services.supplier import SupplierService
from core.dependencies.supplier.supplier_repo import supplier_repo_dep


def supplier_service_dep(repo: SupplierRepository = Depends(supplier_repo_dep)) -> SupplierService:
    return SupplierService(repo)
