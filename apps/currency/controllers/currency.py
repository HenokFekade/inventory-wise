from apps.currency.models.currency import CurrencyModel
from apps.currency.schemas.currency import CurrenciesResponseSchema, CurrencyResponseSchema, CreateCurrencySchema, \
    UpdateCurrencySchema
from apps.currency.services.currency import CurrencyService


class CurrencyController:
    def __init__(self, service: CurrencyService):
        self._service = service

    async def index(self, search: str, per_page: int, page: int) -> CurrenciesResponseSchema:
        return await self._service.index(search=search, per_page=per_page, page=page)

    async def by_id(self, currency: CurrencyModel) -> CurrencyResponseSchema:
        return await self._service.by_id(data=currency)

    async def store(self, data: CreateCurrencySchema) -> CurrencyResponseSchema:
        return await self._service.store(data)

    async def update(self, currency: CurrencyModel, data: UpdateCurrencySchema) -> CurrencyResponseSchema:
        return await self._service.update(data=data, currency=currency)

    async def delete(self, data: CurrencyModel) -> CurrencyResponseSchema:
        return await self._service.delete(data)
