from fastapi import Depends

from apps.tax.repositories.tax import TaxRepository
from apps.tax.services.tax import TaxService
from core.dependencies.tax.tax_repo import tax_repo_dep


def tax_service_dep(repo: TaxRepository = Depends(tax_repo_dep)) -> TaxService:
    return TaxService(repo)
