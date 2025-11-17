from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.customer.repositories.customer import CustomerRepository
from core.dependencies.db import db_dep


def customer_repo_dep(db: AsyncSession = Depends(db_dep)) -> CustomerRepository:
    return CustomerRepository(db)
