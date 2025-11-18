from fastapi import Depends

from apps.item.repositories.item import ItemRepository
from apps.item.schemas.item import UpdateItemSchema
from core.dependencies.item.item_repo import item_repo_dep


async def update_item_validator_dep(
        data: UpdateItemSchema,
        repo: ItemRepository = Depends(item_repo_dep),
) -> UpdateItemSchema:
    return data
