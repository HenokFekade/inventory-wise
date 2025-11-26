from typing import Optional, List, Tuple
from uuid import UUID

from sqlalchemy import select, or_, func, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from apps.account.models.account import AccountModel
from apps.account.schemas.account import CreateAccountModelSchema, UpdateAccountModelSchema
from utils.enums.account_role import AccountRole


class AccountRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    # Optimized query methods
    @staticmethod
    def _base_query():
        return select(AccountModel)

    async def by_pagination(
            self,
            exclude_id: UUID,
            search: str,
            limit: int,
            offset: int,
            role: Optional[AccountRole],
            is_active: Optional[bool],
    ) -> Tuple[List[AccountModel], int]:
        query = self._base_query().filter(
            AccountModel.id != exclude_id,  # type: ignore
            or_(
                AccountModel.first_name.ilike(f"%{search}%"),
                AccountModel.last_name.ilike(f"%{search}%"),
                func.concat(
                    func.coalesce(AccountModel.first_name, ''),
                    ' ',
                    func.coalesce(AccountModel.last_name, '')
                ).ilike(f"%{search}%"),
                AccountModel.username.ilike(f"%{search}%"),
                AccountModel.phone.ilike(f"%{search}%"),
            )
        )
        if role is not None:
            query = query.filter(AccountModel.role == role)  # type: ignore
        if is_active is not None:
            query = query.filter(AccountModel.is_active == is_active)  # type: ignore
        query = query.order_by(AccountModel.created_at.desc())  # type: ignore

        # Use window function for more accurate pagination counts
        result = await self._session.execute(query.limit(limit).offset((offset - 1) * limit))
        results: List[AccountModel] = list(result.scalars().all())
        count_query = select(func.count()).select_from(query.subquery())
        total = await self._session.scalar(count_query)
        return results, total

    async def by_id(self, _id: UUID) -> Optional[AccountModel]:
        query = self._base_query().where(AccountModel.id == _id)  # type: ignore
        return await self._session.scalar(query)

    async def by_username(self, username: str) -> Optional[AccountModel]:
        query = self._base_query().where(AccountModel.username == username)  # type: ignore
        return await self._session.scalar(query)

    async def by_phone(self, phone: str) -> Optional[AccountModel]:
        query = self._base_query().where(AccountModel.phone == phone) # type: ignore
        return await self._session.scalar(query)

    async def store(self, data: CreateAccountModelSchema) -> AccountModel:
        model = AccountModel(**data.model_dump(mode="json")) # type: ignore
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return model

    async def update(self, _id: UUID, data: UpdateAccountModelSchema) -> Optional[AccountModel]:
        values = data.model_dump(exclude_none=True, mode="json")
        if not values:
            return None

        query = update(AccountModel).filter(AccountModel.id == _id).values(values)  # type: ignore
        rows_updated = await self._session.execute(query)
        await self._session.commit()

        if rows_updated == 0:
            return None

        return await self.by_id(_id)

    async def delete(self, _id: UUID):
        query = delete(AccountModel).where(AccountModel.id == _id) # type: ignore
        await self._session.execute(query)
        await self._session.commit()
