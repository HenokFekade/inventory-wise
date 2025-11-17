from uuid import uuid4

from sqlalchemy import Column, UUID, String, Text

from connections.database import BaseDatabase
from utils.models.base_model import TimestampMixin


class SizeModel(TimestampMixin, BaseDatabase):
    __tablename__ = "sizes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(), unique=True, nullable=False)
    description = Column(Text(), nullable=True)
