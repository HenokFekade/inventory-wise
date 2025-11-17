from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.store.repositories.store import StoreRepository
from core.dependencies.db import db_dep


def store_repo_dep(db: AsyncSession = Depends(db_dep)) -> StoreRepository:
    return StoreRepository(db)
