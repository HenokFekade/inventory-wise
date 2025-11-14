from uuid import uuid4

from sqlalchemy import Column, UUID

from connections.database import BaseDatabase
from utils.models.base_model import TimestampMixin


class AuthModel(TimestampMixin, BaseDatabase):
    __tablename__ = "auths"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
