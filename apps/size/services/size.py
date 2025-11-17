from apps.size.models.size import SizeModel
from apps.size.repositories.size import SizeRepository
from apps.size.schemas.size import SizesResponseSchema, SizeSchema, SizeResponseSchema, \
    CreateSizeSchema, CreateSizeModelSchema, UpdateSizeSchema, UpdateSizeModelSchema


class SizeService:
    def __init__(self, repo: SizeRepository):
        self._repo = repo

    async def index(self, search: str, per_page: int, page: int) -> SizesResponseSchema:
        result, total = await self._repo.by_pagination(offset=page, search=search, limit=per_page)
        data = [SizeSchema.model_validate(value) for value in result]
        return SizesResponseSchema(data=data, total=total, page=page, per_page=per_page)

    @staticmethod
    async def by_id(data: SizeModel) -> SizeResponseSchema:
        return SizeResponseSchema(data=SizeSchema.model_validate(data))

    async def store(self, data: CreateSizeSchema) -> SizeResponseSchema:
        data = await self._repo.store(CreateSizeModelSchema(**data.model_dump()))
        return SizeResponseSchema(
            data=SizeSchema.model_validate(data),
            status=201,
            message="Size created successfully",
        )

    async def update(self, size: SizeModel, data: UpdateSizeSchema) -> SizeResponseSchema:
        data = UpdateSizeModelSchema(**data.model_dump())
        result = await self._repo.update(data=data, _id=size.id)
        return SizeResponseSchema(
            data=SizeSchema.model_validate(result),
            message="Size updated successfully",
        )

    async def delete(self, data: SizeModel) -> SizeResponseSchema:
        await self._repo.delete(_id=data.id)
        return SizeResponseSchema(
            data=SizeSchema.model_validate(data),
            message="Size deleted successfully",
        )
