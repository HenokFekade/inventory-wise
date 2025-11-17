from uuid import UUID

from fastapi import Depends, Path

from apps.customer.repositories.customer import CustomerRepository
from apps.customer.schemas.customer import UpdateCustomerSchema
from core.dependencies.customer.customer_repo import customer_repo_dep
from exceptions.unprocessable_entity import UnprocessableEntityException


async def update_customer_validator_dep(
        data: UpdateCustomerSchema,
        _id: UUID = Path(alias="id"),
        repo: CustomerRepository = Depends(customer_repo_dep),
) -> UpdateCustomerSchema:
    result = await repo.by_phone(data.phone)
    if result and result.id != _id:
        UnprocessableEntityException.throw("phone", ["Phone already taken."])
    return data
