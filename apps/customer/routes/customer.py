from typing import Optional

from fastapi import APIRouter, Depends, Query

from apps.customer.controllers.customer import CustomerController
from apps.customer.models.customer import CustomerModel
from apps.customer.schemas.customer import CustomersResponseSchema, CustomerResponseSchema, UpdateCustomerSchema, \
    CreateCustomerSchema
from core.authentications.admin import admin_dep
from core.dependencies import customer_controller_dep, customer_model_binding, create_customer_validator_dep, \
    update_customer_validator_dep

customer_router = APIRouter(prefix="/customers", tags=["Customer"])


@customer_router.get("", response_model=CustomersResponseSchema)
async def index(
        _=Depends(admin_dep),
        page: int = Query(default=1, ge=1),
        per_page: int = Query(default=10, ge=1, alias="per-page"),
        search: Optional[str] = Query(default=""),
        controller: CustomerController = Depends(customer_controller_dep),
):
    return await controller.index(search=search, per_page=per_page, page=page)


@customer_router.post("", response_model=CustomerResponseSchema, status_code=201)
async def create_customer(
        data: CreateCustomerSchema = Depends(create_customer_validator_dep),
        controller: CustomerController = Depends(customer_controller_dep),
        _=Depends(admin_dep),
):
    return await controller.store(data=data)


@customer_router.get("/{id}", response_model=CustomerResponseSchema)
async def get_by_id(
        customer: CustomerModel = Depends(customer_model_binding),
        controller: CustomerController = Depends(customer_controller_dep),
        _=Depends(admin_dep),
):
    return await controller.by_id(customer=customer)


@customer_router.patch("/{id}", response_model=CustomerResponseSchema)
async def update(
        customer: CustomerModel = Depends(customer_model_binding),
        data: UpdateCustomerSchema = Depends(update_customer_validator_dep),
        controller: CustomerController = Depends(customer_controller_dep),
        _=Depends(admin_dep),
):
    return await controller.update(customer=customer, data=data)


@customer_router.delete("/{id}", response_model=CustomerResponseSchema)
async def update(
        customer: CustomerModel = Depends(customer_model_binding),
        controller: CustomerController = Depends(customer_controller_dep),
        _=Depends(admin_dep),
):
    return await controller.delete(data=customer)
