from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.category.repositories.category import CategoryRepository
from core.dependencies.db import db_dep


def category_repo_dep(db: AsyncSession = Depends(db_dep)) -> CategoryRepository:
    return CategoryRepository(db)
