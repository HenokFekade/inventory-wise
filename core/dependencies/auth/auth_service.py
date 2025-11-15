from fastapi import Depends

from apps.account.repositories.account import AccountRepository
from apps.auth.services.auth import AuthService
from core.dependencies.account.account_repo import account_repo_dep

def auth_service_dep(repo: AccountRepository = Depends(account_repo_dep)) -> AuthService:
    return AuthService(repo)

