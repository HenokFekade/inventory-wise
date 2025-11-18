from apps.color.models.color import ColorModel
from apps.color.repositories.color import ColorRepository
from apps.color.schemas.color import ColorsResponseSchema, ColorSchema, ColorResponseSchema, \
    CreateColorSchema, CreateColorModelSchema, UpdateColorSchema, UpdateColorModelSchema


class ColorService:
    def __init__(self, repo: ColorRepository):
        self._repo = repo

    async def index(self, search: str, per_page: int, page: int) -> ColorsResponseSchema:
        result, total = await self._repo.by_pagination(offset=page, search=search, limit=per_page)
        data = [ColorSchema.model_validate(value) for value in result]
        return ColorsResponseSchema(data=data, total=total, page=page, per_page=per_page)

    @staticmethod
    async def by_id(data: ColorModel) -> ColorResponseSchema:
        return ColorResponseSchema(data=ColorSchema.model_validate(data))

    async def store(self, data: CreateColorSchema) -> ColorResponseSchema:
        data = await self._repo.store(CreateColorModelSchema(**data.model_dump()))
        return ColorResponseSchema(
            data=ColorSchema.model_validate(data),
            status=201,
            message="Color created successfully",
        )

    async def update(self, color: ColorModel, data: UpdateColorSchema) -> ColorResponseSchema:
        data = UpdateColorModelSchema(**data.model_dump())
        result = await self._repo.update(data=data, _id=color.id)
        return ColorResponseSchema(
            data=ColorSchema.model_validate(result),
            message="Color updated successfully",
        )

    async def delete(self, data: ColorModel) -> ColorResponseSchema:
        await self._repo.delete(_id=data.id)
        return ColorResponseSchema(
            data=ColorSchema.model_validate(data),
            message="Color deleted successfully",
        )
