from apps.currency.models.currency import CurrencyModel
from apps.currency.repositories.currency import CurrencyRepository
from apps.currency.schemas.currency import CurrenciesResponseSchema, CurrencySchema, CurrencyResponseSchema, \
    CreateCurrencySchema, CreateCurrencyModelSchema, UpdateCurrencySchema, UpdateCurrencyModelSchema


class CurrencyService:
    def __init__(self, repo: CurrencyRepository):
        self._repo = repo

    async def index(self, search: str, per_page: int, page: int) -> CurrenciesResponseSchema:
        result, total = await self._repo.by_pagination(offset=page, search=search, limit=per_page)
        data = [CurrencySchema.model_validate(value) for value in result]
        return CurrenciesResponseSchema(data=data, total=total, page=page, per_page=per_page)

    @staticmethod
    async def by_id(data: CurrencyModel) -> CurrencyResponseSchema:
        return CurrencyResponseSchema(data=CurrencySchema.model_validate(data))

    async def store(self, data: CreateCurrencySchema) -> CurrencyResponseSchema:
        data = await self._repo.store(CreateCurrencyModelSchema(**data.model_dump()))
        return CurrencyResponseSchema(
            data=CurrencySchema.model_validate(data),
            status=201,
            message="Currency created successfully",
        )

    async def update(self, currency: CurrencyModel, data: UpdateCurrencySchema) -> CurrencyResponseSchema:
        data = UpdateCurrencyModelSchema(**data.model_dump())
        result = await self._repo.update(data=data, _id=currency.id)
        return CurrencyResponseSchema(
            data=CurrencySchema.model_validate(result),
            message="Currency updated successfully",
        )

    async def delete(self, data: CurrencyModel) -> CurrencyResponseSchema:
        await self._repo.delete(_id=data.id)
        return CurrencyResponseSchema(
            data=CurrencySchema.model_validate(data),
            message="Currency deleted successfully",
        )
