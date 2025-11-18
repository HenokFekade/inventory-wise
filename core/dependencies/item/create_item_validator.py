from fastapi import Depends

from apps.item.repositories.item import ItemRepository
from apps.item.schemas.item import CreateItemSchema
from core.dependencies.item.item_repo import item_repo_dep


async def create_item_validator_dep(
        data: CreateItemSchema,
        repo: ItemRepository = Depends(item_repo_dep),
) -> CreateItemSchema:
    return data
