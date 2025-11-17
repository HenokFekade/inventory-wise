from typing import Type
from uuid import UUID

from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from apps.store.models.store import StoreModel
from exceptions.not_found import NotFoundException
from core.dependencies.db import db_dep


async def store_model_binding(_id: UUID = Path(alias="id"), db: AsyncSession = Depends(db_dep)) -> Type[StoreModel]:
    instance = await db.get(StoreModel, _id)
    if not instance:
        NotFoundException.throw(f"store not found")
    return instance
