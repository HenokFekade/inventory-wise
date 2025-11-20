from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.store_item.repositories.store_item import StoreItemRepository
from core.dependencies.db import db_dep


def store_item_repo_dep(db: AsyncSession = Depends(db_dep)) -> StoreItemRepository:
    return StoreItemRepository(db)
