from typing import Type
from uuid import UUID

from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from apps.color.models.color import ColorModel
from exceptions.not_found import NotFoundException
from core.dependencies.db import db_dep


async def color_model_binding(_id: UUID = Path(alias="id"), db: AsyncSession = Depends(db_dep)) -> Type[ColorModel]:
    instance = await db.get(ColorModel, _id)
    if not instance:
        NotFoundException.throw(f"color not found")
    return instance
