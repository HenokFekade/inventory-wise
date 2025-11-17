from typing import Type
from uuid import UUID

from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from apps.size.models.size import SizeModel
from exceptions.not_found import NotFoundException
from core.dependencies.db import db_dep


async def size_model_binding(_id: UUID = Path(alias="id"), db: AsyncSession = Depends(db_dep)) -> Type[SizeModel]:
    instance = await db.get(SizeModel, _id)
    if not instance:
        NotFoundException.throw(f"size not found")
    return instance
