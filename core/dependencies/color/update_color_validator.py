from uuid import UUID

from fastapi import Depends, Path

from apps.color.repositories.color import ColorRepository
from apps.color.schemas.color import UpdateColorSchema
from core.dependencies.color.color_repo import color_repo_dep
from exceptions.unprocessable_entity import UnprocessableEntityException


async def update_color_validator_dep(
        data: UpdateColorSchema,
        _id: UUID = Path(alias="id"),
        repo: ColorRepository = Depends(color_repo_dep),
) -> UpdateColorSchema:
    result = await repo.by_name(data.name)
    if result and result.id == _id:
        UnprocessableEntityException.throw("name", ["Name already taken."])
    return data
