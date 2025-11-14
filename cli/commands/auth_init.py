from pathlib import Path

import typer
from rich.console import Console
from utils.install_package import install_package

app = typer.Typer(help="Generate auth init setup for FastAPI project")
console = Console()


@app.command()
def auth_init():
    """Generate auth init setup for FastAPI project."""

    console.print("[bold green]Generating auth init setup...[/bold green]")
    # create token.py file inside core/authentications folder

    install_package("python-jose")
    init_file_path = Path("core") / "__init__.py"
    if not init_file_path.exists():
        init_file_path.write_text("")

    init_path = Path("core/authentications")
    init_path.mkdir(parents=True, exist_ok=True)

    init_file_path = init_path / "__init__.py"
    if not init_file_path.exists():
        init_file_path.write_text("")

    init_path.mkdir(parents=True, exist_ok=True)
    # create __init__.py file inside core/authentications folder
    init_file_path = init_path / "__init__.py"
    if not init_file_path.exists():
        with open(init_file_path, "w") as f:
            f.write("")
    auth_init_file_path = init_path / "token.py"

    with open(auth_init_file_path, "w") as f:
        f.write(f'''from uuid import UUID

from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from apps.account.models.account import AccountModel
from apps.account.repositories.account import AccountRepository
from apps.auth.schemas.auth import TokenSchema
from core.config.config import config
from exceptions.unauthenticated import UnauthenticatedException
from exceptions.unauthorized import UnauthorizedException
from utils.enums.account_role import AccountRole
from utils.enums.token_type import TokenType

class TokenAuth:
    _ALGORITHM = "HS256"
    _AUTH_JWT_SECRET_KEY = config.AUTH_JWT_SECRET_KEY

    def __init__(self, session: AsyncSession):
        self._session = session

    def admin_token(self, _id: UUID, role: AccountRole) -> TokenSchema:
        data = {{"id": str(_id), "role": role.value, "type": TokenType.access_token.value}}
        token = jwt.encode(data, self._AUTH_JWT_SECRET_KEY, algorithm=self._ALGORITHM)
        return TokenSchema(access_token=token)
        
    def decode(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self._AUTH_JWT_SECRET_KEY, algorithms=[self._ALGORITHM])
            if payload.get("id") is None or payload.get("role") is None or payload.get("type") is None:
                UnauthorizedException.throw()
            return payload.copy()
        except JWTError:
            UnauthenticatedException.throw()
    
    async def _check_account_is_active(self, account_id: UUID) -> AccountModel:
        account = await AccountRepository(self._session).by_id(_id=account_id)
        if account is None:
            UnauthorizedException.throw()
        elif not account.is_active:
            UnauthorizedException.throw()
        elif not account.is_verified:
            UnauthorizedException.throw()

        return account
        
    async def super_admin_only(self, token: str) -> AccountModel:
        payload = self.decode(token)
        _id = payload.get("id")
        _type = payload.get("role")
        if _id is None or _type is None or _type != AccountRole.super_admin.value:
            UnauthorizedException.throw()
        return await self._check_account_is_active(_id)

''')

    init_file_path = init_path / "__init__.py"
    # check if init.py exists
    if not init_file_path.exists():
        with open(init_file_path, "w") as f:
            f.write("")

    console.print("[bold green]auth init setup generated successfully![/bold green]")
