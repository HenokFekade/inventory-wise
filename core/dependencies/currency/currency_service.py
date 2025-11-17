from fastapi import Depends

from apps.currency.repositories.currency import CurrencyRepository
from apps.currency.services.currency import CurrencyService
from core.dependencies.currency.currency_repo import currency_repo_dep


def currency_service_dep(repo: CurrencyRepository = Depends(currency_repo_dep)) -> CurrencyService:
    return CurrencyService(repo)
