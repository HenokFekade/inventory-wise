from apps.size.models.size import SizeModel
from apps.size.schemas.size import SizesResponseSchema, SizeResponseSchema, CreateSizeSchema, \
    UpdateSizeSchema
from apps.size.services.size import SizeService


class SizeController:
    def __init__(self, service: SizeService):
        self._service = service

    async def index(self, search: str, per_page: int, page: int) -> SizesResponseSchema:
        return await self._service.index(search=search, per_page=per_page, page=page)

    async def by_id(self, size: SizeModel) -> SizeResponseSchema:
        return await self._service.by_id(data=size)

    async def store(self, data: CreateSizeSchema) -> SizeResponseSchema:
        return await self._service.store(data)

    async def update(self, size: SizeModel, data: UpdateSizeSchema) -> SizeResponseSchema:
        return await self._service.update(data=data, size=size)

    async def delete(self, data: SizeModel) -> SizeResponseSchema:
        return await self._service.delete(data)
