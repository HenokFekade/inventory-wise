from typing import Type
from uuid import UUID

from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from apps.currency.models.currency import CurrencyModel
from exceptions.not_found import NotFoundException
from core.dependencies.db import db_dep


async def currency_model_binding(_id: UUID = Path(alias="id"), db: AsyncSession = Depends(db_dep)) -> Type[
    CurrencyModel]:
    instance = await db.get(CurrencyModel, _id)
    if not instance:
        NotFoundException.throw(f"currency not found")
    return instance
