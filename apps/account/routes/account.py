from typing import Optional

from fastapi import APIRouter, Depends, Query

from apps.account.controllers.account import AccountController
from apps.account.models.account import AccountModel
from apps.account.schemas.account import AccountsResponseSchema, AccountResponseSchema, UpdateAccountSchema, \
    ChangePasswordSchema, CreateAccountSchema
from core.authentications.super_admin import super_admin_dep
from core.dependencies import account_controller_dep, account_model_binding
from utils.enums.account_role import AccountRole

account_router = APIRouter(prefix="/accounts", tags=["Account"])


@account_router.get("", response_model=AccountsResponseSchema)
async def index(
        account: AccountModel = Depends(super_admin_dep),
        page: int = Query(default=1, ge=1),
        per_page: int = Query(default=10, ge=1, alias="per-page"),
        search: Optional[str] = Query(default=""),
        role: Optional[AccountRole] = Query(default=None),
        is_active: Optional[bool] = Query(default=None),
        controller: AccountController = Depends(account_controller_dep),
):
    return await controller.index(
        is_active=is_active,
        search=search,
        role=role,
        account=account,
        per_page=per_page,
        page=page,
    )


@account_router.post("", response_model=AccountResponseSchema, status_code=201)
async def create_account(
        data: CreateAccountSchema,
        controller: AccountController = Depends(account_controller_dep),
        _=Depends(super_admin_dep),
):
    return await controller.store(data=data)


@account_router.put("/change-password", response_model=AccountResponseSchema)
async def change_password(
        data: ChangePasswordSchema,
        controller: AccountController = Depends(account_controller_dep),
        account: AccountModel = Depends(super_admin_dep),
):
    return await controller.change_password(account=account.id, data=data)


@account_router.get("/{id}", response_model=AccountResponseSchema)
async def get_by_id(
        account: AccountModel = Depends(account_model_binding),
        controller: AccountController = Depends(account_controller_dep),
        _=Depends(super_admin_dep),
):
    return await controller.by_id(account)


@account_router.patch("/{id}", response_model=AccountResponseSchema)
async def update(
        data: UpdateAccountSchema,
        account: AccountModel = Depends(account_model_binding),
        controller: AccountController = Depends(account_controller_dep),
        _=Depends(super_admin_dep),
):
    return await controller.update(account=account, data=data)


@account_router.delete("/{id}", response_model=AccountResponseSchema)
async def update(
        account: AccountModel = Depends(account_model_binding),
        controller: AccountController = Depends(account_controller_dep),
        _=Depends(super_admin_dep),
):
    return await controller.delete(data=account)
