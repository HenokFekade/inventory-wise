from fastapi import Depends

from apps.account.repositories.account import AccountRepository
from apps.account.services.account import AccountService
from core.dependencies.account_repo import account_repo_dep


def account_service_dep(repo: AccountRepository = Depends(account_repo_dep)) -> AccountService:
    return AccountService(repo)
