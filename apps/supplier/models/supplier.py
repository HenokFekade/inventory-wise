from uuid import uuid4

from sqlalchemy import Column, UUID, String, Text

from connections.database import BaseDatabase
from utils.models.base_model import TimestampMixin


class SupplierModel(TimestampMixin, BaseDatabase):
    __tablename__ = "suppliers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(), nullable=False)
    phone = Column(String(), unique=True, nullable=False)
    address = Column(String(), nullable=True)
    note = Column(Text(), nullable=True)
