from uuid import uuid4

from sqlalchemy import Column, UUID, String, Enum, Boolean

from connections.database import BaseDatabase
from utils.enums.account_role import AccountRole
from utils.models.base_model import TimestampMixin

            
             
class AccountModel(TimestampMixin, BaseDatabase):
    __tablename__ = "accounts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    first_name = Column(String(), nullable=False)
    last_name = Column(String(), nullable=False)
    role = Column(Enum(AccountRole), nullable=False)
    phone = Column(String(), nullable=False, unique=True)
    email = Column(String(), nullable=False, unique=True)
    password = Column(String(), nullable=False)
    password_change_required = Column(Boolean(), nullable=False)
    is_active = Column(Boolean(), nullable=False, default=True)
    image = Column(String(), nullable=True)
