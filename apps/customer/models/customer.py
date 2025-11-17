from uuid import uuid4

from sqlalchemy import Column, UUID, String, Text

from connections.database import BaseDatabase
from utils.models.base_model import TimestampMixin


class CustomerModel(TimestampMixin, BaseDatabase):
    __tablename__ = "customers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(), nullable=False)
    phone = Column(String(), unique=True, nullable=False)
    house_number = Column(String(), nullable=False)
    country = Column(String(), nullable=True)
    city = Column(String(), nullable=True)
    note = Column(Text(), nullable=True)
    additional_phone = Column(String(), nullable=True)
