from apps.supplier.models.supplier import SupplierModel
from apps.supplier.repositories.supplier import SupplierRepository
from apps.supplier.schemas.supplier import SuppliersResponseSchema, SupplierSchema, SupplierResponseSchema, \
    CreateSupplierSchema, CreateSupplierModelSchema, UpdateSupplierSchema, UpdateSupplierModelSchema


class SupplierService:
    def __init__(self, repo: SupplierRepository):
        self._repo = repo

    async def index(self, search: str, per_page: int, page: int) -> SuppliersResponseSchema:
        result, total = await self._repo.by_pagination(offset=page, search=search, limit=per_page)
        data = [SupplierSchema.model_validate(value) for value in result]
        return SuppliersResponseSchema(data=data, total=total, page=page, per_page=per_page)

    @staticmethod
    async def by_id(data: SupplierModel) -> SupplierResponseSchema:
        return SupplierResponseSchema(data=SupplierSchema.model_validate(data))

    async def store(self, data: CreateSupplierSchema) -> SupplierResponseSchema:
        data = await self._repo.store(CreateSupplierModelSchema(**data.model_dump()))
        return SupplierResponseSchema(
            data=SupplierSchema.model_validate(data),
            status=201,
            message="Supplier created successfully",
        )

    async def update(self, supplier: SupplierModel, data: UpdateSupplierSchema) -> SupplierResponseSchema:
        data = UpdateSupplierModelSchema(**data.model_dump())
        result = await self._repo.update(data=data, _id=supplier.id)
        return SupplierResponseSchema(
            data=SupplierSchema.model_validate(result),
            message="Supplier updated successfully",
        )

    async def delete(self, data: SupplierModel) -> SupplierResponseSchema:
        await self._repo.delete(_id=data.id)
        return SupplierResponseSchema(
            data=SupplierSchema.model_validate(data),
            message="Supplier deleted successfully",
        )
