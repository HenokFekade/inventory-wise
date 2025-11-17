from uuid import UUID

from fastapi import Depends, Path

from apps.size.repositories.size import SizeRepository
from apps.size.schemas.size import UpdateSizeSchema
from core.dependencies.size.size_repo import size_repo_dep
from exceptions.unprocessable_entity import UnprocessableEntityException


async def update_size_validator_dep(
        data: UpdateSizeSchema,
        _id: UUID = Path(alias="id"),
        repo: SizeRepository = Depends(size_repo_dep),
) -> UpdateSizeSchema:
    if data.name:
        result = await repo.by_name(data.name)
        if result and result.id != _id:
            UnprocessableEntityException.throw("name", ["Name already taken."])
    return data
