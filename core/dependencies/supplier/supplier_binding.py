from typing import Type
from uuid import UUID

from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from apps.supplier.models.supplier import SupplierModel
from exceptions.not_found import NotFoundException
from core.dependencies.db import db_dep


async def supplier_model_binding(_id: UUID = Path(alias="id"), db: AsyncSession = Depends(db_dep)) -> Type[
    SupplierModel]:
    instance = await db.get(SupplierModel, _id)
    if not instance:
        NotFoundException.throw(f"supplier not found")
    return instance
