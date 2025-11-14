from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from core.config.config import config


engine = create_async_engine(config.DATABASE_URL, pool_size=100, max_overflow=200, pool_timeout=30, pool_recycle=1800)

AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)

BaseDatabase = declarative_base()

