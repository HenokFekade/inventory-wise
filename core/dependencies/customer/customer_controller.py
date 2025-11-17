from fastapi import Depends

from apps.customer.services.customer import CustomerService
from apps.customer.controllers.customer import CustomerController
from core.dependencies.customer.customer_service import customer_service_dep


def customer_controller_dep(service: CustomerService = Depends(customer_service_dep)) -> CustomerController:
    return CustomerController(service)
