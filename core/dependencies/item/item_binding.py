from typing import Type
from uuid import UUID

from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from apps.item.models.item import ItemModel
from exceptions.not_found import NotFoundException
from core.dependencies.db import db_dep


async def item_model_binding(_id: UUID = Path(alias="id"), db: AsyncSession = Depends(db_dep)) -> Type[ItemModel]:
    instance = await db.get(ItemModel, _id)
    if not instance:
        NotFoundException.throw(f"item not found")
    return instance
