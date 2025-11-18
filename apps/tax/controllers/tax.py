from apps.tax.models.tax import TaxModel
from apps.tax.schemas.tax import TaxsResponseSchema, TaxResponseSchema, CreateTaxSchema, \
    UpdateTaxSchema
from apps.tax.services.tax import TaxService


class TaxController:
    def __init__(self, service: TaxService):
        self._service = service

    async def index(self, search: str, per_page: int, page: int) -> TaxsResponseSchema:
        return await self._service.index(search=search, per_page=per_page, page=page)

    async def by_id(self, tax: TaxModel) -> TaxResponseSchema:
        return await self._service.by_id(data=tax)

    async def store(self, data: CreateTaxSchema) -> TaxResponseSchema:
        return await self._service.store(data)

    async def update(self, tax: TaxModel, data: UpdateTaxSchema) -> TaxResponseSchema:
        return await self._service.update(data=data, tax=tax)

    async def delete(self, data: TaxModel) -> TaxResponseSchema:
        return await self._service.delete(data)
