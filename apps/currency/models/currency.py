from uuid import uuid4

from sqlalchemy import Column, UUID, String

from connections.database import BaseDatabase
from utils.models.base_model import TimestampMixin


class CurrencyModel(TimestampMixin, BaseDatabase):
    __tablename__ = "currencies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(), unique=True, nullable=False)
    code = Column(String(), unique=True, nullable=False)
