from fastapi import Depends

from apps.account.controllers.account import AccountController
from apps.account.services.account import AccountService
from core.dependencies.account_service import account_service_dep


def account_controller_dep(service: AccountService = Depends(account_service_dep)) -> AccountController:
    return AccountController(service)
