from fastapi import Depends

from apps.customer.repositories.customer import CustomerRepository
from apps.customer.services.customer import CustomerService
from core.dependencies.customer.customer_repo import customer_repo_dep


def customer_service_dep(repo: CustomerRepository = Depends(customer_repo_dep)) -> CustomerService:
    return CustomerService(repo)
