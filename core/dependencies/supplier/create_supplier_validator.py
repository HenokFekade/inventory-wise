from fastapi import Depends

from apps.supplier.repositories.supplier import SupplierRepository
from apps.supplier.schemas.supplier import CreateSupplierSchema
from core.dependencies.supplier.supplier_repo import supplier_repo_dep
from exceptions.unprocessable_entity import UnprocessableEntityException


async def create_supplier_validator_dep(
        data: CreateSupplierSchema,
        repo: SupplierRepository = Depends(supplier_repo_dep),
) -> CreateSupplierSchema:
    result = await repo.by_phone(data.phone)
    if result:
        UnprocessableEntityException.throw("phone", ["Phone already taken."])
    return data
