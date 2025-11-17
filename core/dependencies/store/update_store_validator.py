from uuid import UUID

from fastapi import Depends, Path

from apps.store.repositories.store import StoreRepository
from apps.store.schemas.store import UpdateStoreSchema
from core.dependencies.store.store_repo import store_repo_dep
from exceptions.unprocessable_entity import UnprocessableEntityException


async def update_store_validator_dep(
        data: UpdateStoreSchema,
        _id: UUID = Path(alias="id"),
        repo: StoreRepository = Depends(store_repo_dep),
) -> UpdateStoreSchema:
    result = await repo.by_name(data.name)
    if result and result.id != _id:
        UnprocessableEntityException.throw("name", ["Name already taken."])
    return data
