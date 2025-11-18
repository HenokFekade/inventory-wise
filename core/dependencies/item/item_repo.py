from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.item.repositories.item import ItemRepository
from core.dependencies.db import db_dep


def item_repo_dep(db: AsyncSession = Depends(db_dep)) -> ItemRepository:
    return ItemRepository(db)
