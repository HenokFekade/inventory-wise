from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.account.repositories.account import AccountRepository
from core.dependencies.db import db_dep


def account_repo_dep(db: AsyncSession = Depends(db_dep)) -> AccountRepository:
    return AccountRepository(db)

