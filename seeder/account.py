from sqlalchemy import func, select

from apps.account.models.account import AccountModel
from connections.database import AsyncSessionLocal
from utils.enums.account_role import AccountRole
from utils.password import PasswordHelper


async def account_seeder():
    async with AsyncSessionLocal() as session:
        query = select(func.count(AccountModel.id))
        count = await session.scalar(query)
        if count == 0:
            data = AccountModel(
                first_name="Super", # type: ignore
                last_name="Admin", # type: ignore
                email="superadmin@gmail.com", # type: ignore
                phone="+251912345678", # type: ignore
                password=PasswordHelper.hash("P@ssw0rd"), # type: ignore
                role=AccountRole.super_admin, # type: ignore
                is_active=True, # type: ignore
                password_change_required=True # type: ignore
            )
            session.add(data)
            await session.commit()
            print(f'Default account created with email: "{data.email}" and password: "passw0rd"')
        else:
            print(f'Default account already created')
        await session.close()