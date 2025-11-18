from uuid import uuid4

from sqlalchemy import Column, UUID, String, Double, ForeignKey, Integer, Boolean, Text, ARRAY
from sqlalchemy.orm import relationship

from connections.database import BaseDatabase
from utils.models.base_model import TimestampMixin


class ItemModel(TimestampMixin, BaseDatabase):
    __tablename__ = "items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(), nullable=False)
    code = Column(String(), nullable=True)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False)
    color_id = Column(UUID(as_uuid=True), ForeignKey("colors.id"), nullable=True)
    size_id = Column(UUID(as_uuid=True), ForeignKey("sizes.id"), nullable=True)
    currency_id = Column(UUID(as_uuid=True), ForeignKey("currencies.id"), nullable=False)
    unit_id = Column(UUID(as_uuid=True), ForeignKey("units.id"), nullable=False)
    tax_id = Column(UUID(as_uuid=True), ForeignKey("taxes.id"), nullable=False)
    unit_cost = Column(Double(), nullable=False)
    selling_price = Column(Double(), nullable=False)
    min_selling_price = Column(Double(), nullable=False)
    warning_quantity = Column(Integer(), nullable=False)
    is_publicly_visible = Column(Boolean(), nullable=False)
    description = Column(Text(), nullable=True)
    images = Column(ARRAY(String), nullable=False)
    category = relationship("CategoryModel", uselist=False)
    color = relationship("ColorModel", uselist=False)
    size = relationship("SizeModel", uselist=False)
    currency = relationship("CurrencyModel", uselist=False)
    unit = relationship("UnitModel", uselist=False)
    tax = relationship("TaxModel", uselist=False)
