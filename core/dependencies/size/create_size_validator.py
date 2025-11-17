from fastapi import Depends

from apps.size.repositories.size import SizeRepository
from apps.size.schemas.size import CreateSizeSchema
from core.dependencies.size.size_repo import size_repo_dep
from exceptions.unprocessable_entity import UnprocessableEntityException


async def create_size_validator_dep(
        data: CreateSizeSchema,
        repo: SizeRepository = Depends(size_repo_dep),
) -> CreateSizeSchema:
    result = await repo.by_name(data.name)
    if result:
        UnprocessableEntityException.throw("name", ["Name already taken."])
    return data
