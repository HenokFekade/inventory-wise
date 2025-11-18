from apps.tax.models.tax import TaxModel
from apps.tax.repositories.tax import TaxRepository
from apps.tax.schemas.tax import TaxsResponseSchema, TaxSchema, TaxResponseSchema, \
    CreateTaxSchema, CreateTaxModelSchema, UpdateTaxSchema, UpdateTaxModelSchema


class TaxService:
    def __init__(self, repo: TaxRepository):
        self._repo = repo

    async def index(self, search: str, per_page: int, page: int) -> TaxsResponseSchema:
        result, total = await self._repo.by_pagination(offset=page, search=search, limit=per_page)
        data = [TaxSchema.model_validate(value) for value in result]
        return TaxsResponseSchema(data=data, total=total, page=page, per_page=per_page)

    @staticmethod
    async def by_id(data: TaxModel) -> TaxResponseSchema:
        return TaxResponseSchema(data=TaxSchema.model_validate(data))

    async def store(self, data: CreateTaxSchema) -> TaxResponseSchema:
        data = await self._repo.store(CreateTaxModelSchema(**data.model_dump()))
        return TaxResponseSchema(
            data=TaxSchema.model_validate(data),
            status=201,
            message="Tax created successfully",
        )

    async def update(self, tax: TaxModel, data: UpdateTaxSchema) -> TaxResponseSchema:
        data = UpdateTaxModelSchema(**data.model_dump())
        result = await self._repo.update(data=data, _id=tax.id)
        return TaxResponseSchema(
            data=TaxSchema.model_validate(result),
            message="Tax updated successfully",
        )

    async def delete(self, data: TaxModel) -> TaxResponseSchema:
        await self._repo.delete(_id=data.id)
        return TaxResponseSchema(
            data=TaxSchema.model_validate(data),
            message="Tax deleted successfully",
        )
