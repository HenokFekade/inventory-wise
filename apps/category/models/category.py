from uuid import uuid4

from sqlalchemy import Column, UUID, String, ARRAY, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from connections.database import BaseDatabase
from utils.models.base_model import TimestampMixin


class CategoryModel(TimestampMixin, BaseDatabase):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True)
    images = Column(ARRAY(String), nullable=True)
    is_active = Column(Boolean(), nullable=False, default=True)
    is_publicly_visible = Column(Boolean(), nullable=False)
    sub_categories = relationship("CategoryModel", foreign_keys=[category_id], remote_side=[id], uselist=True)
