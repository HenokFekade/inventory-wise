from uuid import UUID

from fastapi import Depends, Path

from apps.supplier.repositories.supplier import SupplierRepository
from apps.supplier.schemas.supplier import UpdateSupplierSchema
from core.dependencies.supplier.supplier_repo import supplier_repo_dep
from exceptions.unprocessable_entity import UnprocessableEntityException


async def update_supplier_validator_dep(
        data: UpdateSupplierSchema,
        _id: UUID = Path(alias="id"),
        repo: SupplierRepository = Depends(supplier_repo_dep),
) -> UpdateSupplierSchema:
    if data.phone:
        result = await repo.by_phone(data.phone)
        if result and result.id != _id:
            UnprocessableEntityException.throw("phone", ["Phone already taken."])
    return data
