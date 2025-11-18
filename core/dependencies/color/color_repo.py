from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.color.repositories.color import ColorRepository
from core.dependencies.db import db_dep


def color_repo_dep(db: AsyncSession = Depends(db_dep)) -> ColorRepository:
    return ColorRepository(db)
