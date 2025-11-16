from typing import Type
from uuid import UUID

from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from apps.category.models.category import CategoryModel
from exceptions.not_found import NotFoundException
from core.dependencies.db import db_dep


async def category_model_binding(_id: UUID = Path(alias="id"), db: AsyncSession = Depends(db_dep)) -> Type[
    CategoryModel]:
    instance = await db.get(CategoryModel, _id)
    if not instance:
        NotFoundException.throw(f"category not found")
    return instance
