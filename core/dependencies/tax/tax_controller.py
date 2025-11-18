from fastapi import Depends

from apps.tax.services.tax import TaxService
from apps.tax.controllers.tax import TaxController
from core.dependencies.tax.tax_service import tax_service_dep


def tax_controller_dep(service: TaxService = Depends(tax_service_dep)) -> TaxController:
    return TaxController(service)
