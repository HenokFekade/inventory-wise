from uuid import uuid4

from sqlalchemy import Column, UUID, ForeignKey, BigInteger, UniqueConstraint

from connections.database import BaseDatabase
from utils.models.base_model import TimestampMixin


class StoreItemModel(TimestampMixin, BaseDatabase):
    __tablename__ = "store_items"
    __table_args__ = (UniqueConstraint("item_id", "store_id", name="uni_store_item"),)

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    item_id = Column(UUID(as_uuid=True), ForeignKey("items.id", ondelete="cascade"), nullable=False)
    store_id = Column(UUID(as_uuid=True), ForeignKey("stores.id", ondelete="cascade"), nullable=False)
    quantity = Column(BigInteger(), nullable=False)
