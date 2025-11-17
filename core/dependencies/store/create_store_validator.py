from fastapi import Depends

from apps.store.repositories.store import StoreRepository
from apps.store.schemas.store import CreateStoreSchema
from core.dependencies.store.store_repo import store_repo_dep
from exceptions.unprocessable_entity import UnprocessableEntityException


async def create_store_validator_dep(
        data: CreateStoreSchema,
        repo: StoreRepository = Depends(store_repo_dep),
) -> CreateStoreSchema:
    result = await repo.by_name(data.name)
    if result:
        UnprocessableEntityException.throw("name", ["Name already taken."])
    return data
