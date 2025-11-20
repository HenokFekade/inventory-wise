from typing import Type
from uuid import UUID

from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from apps.store_item.models.store_item import StoreItemModel
from exceptions.not_found import NotFoundException
from core.dependencies.db import db_dep


async def store_item_model_binding(_id: UUID = Path(alias="id"), db: AsyncSession = Depends(db_dep)) -> Type[
    StoreItemModel]:
    instance = await db.get(StoreItemModel, _id)
    if not instance:
        NotFoundException.throw(f"store item not found")
    return instance
