from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.currency.repositories.currency import CurrencyRepository
from core.dependencies.db import db_dep


def currency_repo_dep(db: AsyncSession = Depends(db_dep)) -> CurrencyRepository:
    return CurrencyRepository(db)
