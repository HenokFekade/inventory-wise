from connections.database import AsyncSessionLocal


async def db_dep():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()
