from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.size.repositories.size import SizeRepository
from core.dependencies.db import db_dep


def size_repo_dep(db: AsyncSession = Depends(db_dep)) -> SizeRepository:
    return SizeRepository(db)
