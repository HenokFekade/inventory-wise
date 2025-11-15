from typing import Type
from uuid import UUID

from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from apps.account.models.account import AccountModel
from core.dependencies.db import db_dep
from exceptions.not_found import NotFoundException


async def account_model_binding(_id: UUID = Path(alias="id"), db: AsyncSession = Depends(db_dep)) -> Type[AccountModel]:
    instance = await db.get(AccountModel, _id)
    if not instance:
        NotFoundException.throw(f"account not found")
    return instance
