from apps.color.models.color import ColorModel
from apps.color.schemas.color import ColorsResponseSchema, ColorResponseSchema, CreateColorSchema, \
    UpdateColorSchema
from apps.color.services.color import ColorService


class ColorController:
    def __init__(self, service: ColorService):
        self._service = service

    async def index(self, search: str, per_page: int, page: int) -> ColorsResponseSchema:
        return await self._service.index(search=search, per_page=per_page, page=page)

    async def by_id(self, color: ColorModel) -> ColorResponseSchema:
        return await self._service.by_id(data=color)

    async def store(self, data: CreateColorSchema) -> ColorResponseSchema:
        return await self._service.store(data)

    async def update(self, color: ColorModel, data: UpdateColorSchema) -> ColorResponseSchema:
        return await self._service.update(data=data, color=color)

    async def delete(self, data: ColorModel) -> ColorResponseSchema:
        return await self._service.delete(data)
