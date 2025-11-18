from apps.supplier.models.supplier import SupplierModel
from apps.supplier.schemas.supplier import SuppliersResponseSchema, SupplierResponseSchema, CreateSupplierSchema, \
    UpdateSupplierSchema
from apps.supplier.services.supplier import SupplierService


class SupplierController:
    def __init__(self, service: SupplierService):
        self._service = service

    async def index(self, search: str, per_page: int, page: int) -> SuppliersResponseSchema:
        return await self._service.index(search=search, per_page=per_page, page=page)

    async def by_id(self, supplier: SupplierModel) -> SupplierResponseSchema:
        return await self._service.by_id(data=supplier)

    async def store(self, data: CreateSupplierSchema) -> SupplierResponseSchema:
        return await self._service.store(data)

    async def update(self, supplier: SupplierModel, data: UpdateSupplierSchema) -> SupplierResponseSchema:
        return await self._service.update(data=data, supplier=supplier)

    async def delete(self, data: SupplierModel) -> SupplierResponseSchema:
        return await self._service.delete(data)
