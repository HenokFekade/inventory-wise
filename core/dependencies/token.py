from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.authentications.token import TokenAuth
from core.dependencies.db import db_dep


def token_dep(db: AsyncSession = Depends(db_dep)) -> TokenAuth:
    return TokenAuth(db)
