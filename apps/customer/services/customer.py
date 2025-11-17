from apps.customer.models.customer import CustomerModel
from apps.customer.repositories.customer import CustomerRepository
from apps.customer.schemas.customer import CustomersResponseSchema, CustomerSchema, CustomerResponseSchema, \
    CreateCustomerSchema, CreateCustomerModelSchema, UpdateCustomerSchema, UpdateCustomerModelSchema


class CustomerService:
    def __init__(self, repo: CustomerRepository):
        self._repo = repo

    async def index(self, search: str, per_page: int, page: int) -> CustomersResponseSchema:
        result, total = await self._repo.by_pagination(offset=page, search=search, limit=per_page)
        data = [CustomerSchema.model_validate(value) for value in result]
        return CustomersResponseSchema(data=data, total=total, page=page, per_page=per_page)

    @staticmethod
    async def by_id(data: CustomerModel) -> CustomerResponseSchema:
        return CustomerResponseSchema(data=CustomerSchema.model_validate(data))

    async def store(self, data: CreateCustomerSchema) -> CustomerResponseSchema:
        data = await self._repo.store(CreateCustomerModelSchema(**data.model_dump()))
        return CustomerResponseSchema(
            data=CustomerSchema.model_validate(data),
            status=201,
            message="Customer created successfully",
        )

    async def update(self, customer: CustomerModel, data: UpdateCustomerSchema) -> CustomerResponseSchema:
        data = UpdateCustomerModelSchema(**data.model_dump())
        result = await self._repo.update(data=data, _id=customer.id)
        return CustomerResponseSchema(
            data=CustomerSchema.model_validate(result),
            message="Customer updated successfully",
        )

    async def delete(self, data: CustomerModel) -> CustomerResponseSchema:
        await self._repo.delete(_id=data.id)
        return CustomerResponseSchema(
            data=CustomerSchema.model_validate(data),
            message="Customer deleted successfully",
        )
