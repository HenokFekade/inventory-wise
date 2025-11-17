from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.unit.repositories.unit import UnitRepository
from core.dependencies.db import db_dep


def unit_repo_dep(db: AsyncSession = Depends(db_dep)) -> UnitRepository:
    return UnitRepository(db)
