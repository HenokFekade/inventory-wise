from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.supplier.repositories.supplier import SupplierRepository
from core.dependencies.db import db_dep


def supplier_repo_dep(db: AsyncSession = Depends(db_dep)) -> SupplierRepository:
    return SupplierRepository(db)
