from typing import Type
from uuid import UUID

from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from apps.tax.models.tax import TaxModel
from exceptions.not_found import NotFoundException
from core.dependencies.db import db_dep


async def tax_model_binding(_id: UUID = Path(alias="id"), db: AsyncSession = Depends(db_dep)) -> Type[TaxModel]:
    instance = await db.get(TaxModel, _id)
    if not instance:
        NotFoundException.throw(f"tax not found")
    return instance
