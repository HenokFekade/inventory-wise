from fastapi import Depends

from apps.currency.services.currency import CurrencyService
from apps.currency.controllers.currency import CurrencyController
from core.dependencies.currency.currency_service import currency_service_dep


def currency_controller_dep(service: CurrencyService = Depends(currency_service_dep)) -> CurrencyController:
    return CurrencyController(service)
