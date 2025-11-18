from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.tax.repositories.tax import TaxRepository
from core.dependencies.db import db_dep


def tax_repo_dep(db: AsyncSession = Depends(db_dep)) -> TaxRepository:
    return TaxRepository(db)
