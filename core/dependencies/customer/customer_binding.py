from typing import Type
from uuid import UUID

from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from apps.customer.models.customer import CustomerModel
from exceptions.not_found import NotFoundException
from core.dependencies.db import db_dep


async def customer_model_binding(_id: UUID = Path(alias="id"), db: AsyncSession = Depends(db_dep)) -> Type[
    CustomerModel]:
    instance = await db.get(CustomerModel, _id)
    if not instance:
        NotFoundException.throw(f"customer not found")
    return instance
