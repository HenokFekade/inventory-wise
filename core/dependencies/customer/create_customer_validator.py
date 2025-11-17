from fastapi import Depends

from apps.customer.repositories.customer import CustomerRepository
from apps.customer.schemas.customer import CreateCustomerSchema
from core.dependencies.customer.customer_repo import customer_repo_dep
from exceptions.unprocessable_entity import UnprocessableEntityException


async def create_customer_validator_dep(
        data: CreateCustomerSchema,
        repo: CustomerRepository = Depends(customer_repo_dep),
) -> CreateCustomerSchema:
    result = await repo.by_phone(data.phone)
    if result:
        UnprocessableEntityException.throw("phone", ["Phone already taken."])
    return data
