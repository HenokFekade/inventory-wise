from fastapi import Depends

from apps.color.repositories.color import ColorRepository
from apps.color.schemas.color import CreateColorSchema
from core.dependencies.color.color_repo import color_repo_dep
from exceptions.unprocessable_entity import UnprocessableEntityException


async def create_color_validator_dep(
        data: CreateColorSchema,
        repo: ColorRepository = Depends(color_repo_dep),
) -> CreateColorSchema:
    result = await repo.by_name(data.name)
    if result:
        UnprocessableEntityException.throw("name", ["Name already taken."])
    return data
