from uuid import uuid4

from sqlalchemy import Column, UUID, Integer, Text

from connections.database import BaseDatabase
from utils.models.base_model import TimestampMixin


class TaxModel(TimestampMixin, BaseDatabase):
    __tablename__ = "taxes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    percent = Column(Integer(), unique=True, nullable=False)
    description = Column(Text(), nullable=True)
