from typing import Type
from uuid import UUID

from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from apps.unit.models.unit import UnitModel
from exceptions.not_found import NotFoundException
from core.dependencies.db import db_dep


async def unit_model_binding(_id: UUID = Path(alias="id"), db: AsyncSession = Depends(db_dep)) -> Type[UnitModel]:
    instance = await db.get(UnitModel, _id)
    if not instance:
        NotFoundException.throw(f"unit not found")
    return instance
