from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.auth.models.auth import AuthModel


class AuthRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    # Optimized query methods
    @staticmethod
    def _base_query():
        return select(AuthModel)
