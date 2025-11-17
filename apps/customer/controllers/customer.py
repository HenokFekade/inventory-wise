from apps.customer.models.customer import CustomerModel
from apps.customer.schemas.customer import CustomersResponseSchema, CustomerResponseSchema, CreateCustomerSchema, \
    UpdateCustomerSchema
from apps.customer.services.customer import CustomerService


class CustomerController:
    def __init__(self, service: CustomerService):
        self._service = service

    async def index(self, search: str, per_page: int, page: int) -> CustomersResponseSchema:
        return await self._service.index(search=search, per_page=per_page, page=page)

    async def by_id(self, customer: CustomerModel) -> CustomerResponseSchema:
        return await self._service.by_id(data=customer)

    async def store(self, data: CreateCustomerSchema) -> CustomerResponseSchema:
        return await self._service.store(data)

    async def update(self, customer: CustomerModel, data: UpdateCustomerSchema) -> CustomerResponseSchema:
        return await self._service.update(data=data, customer=customer)

    async def delete(self, data: CustomerModel) -> CustomerResponseSchema:
        return await self._service.delete(data)
