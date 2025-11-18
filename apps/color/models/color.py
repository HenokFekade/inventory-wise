from uuid import uuid4

from sqlalchemy import Column, UUID, String

from connections.database import BaseDatabase
from utils.models.base_model import TimestampMixin


class ColorModel(TimestampMixin, BaseDatabase):
    __tablename__ = "colors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(), unique=True, nullable=False)
