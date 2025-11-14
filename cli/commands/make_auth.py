from pathlib import Path

import typer
from rich.console import Console

app = typer.Typer(help="Generate auth  setup for FastAPI project")
console = Console()


@app.command()
def make_auth(
        name: str = typer.Argument(..., help="Name of the Authentication"),
):
    """Generate auth  setup for FastAPI project."""

    console.print("[bold green]Generating auth  setup...[/bold green]")
    # create token.py file inside core/authentications folder

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
    auth_init_file_path = init_path / f"{name.lower()}.py"

    with open(auth_init_file_path, "w") as f:
        f.write(f'''from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from apps.account.models.account import AccountModel
from core.authentications.token import TokenAuth
from core.dependencies.token import token_dep

_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def {name}_dep(
        token: Annotated[str, Depends(_oauth2_scheme)],
        token_auth: TokenAuth = Depends(token_dep),
) -> AccountModel:
    return await token_auth.{name}(token)

''')

    init_file_path = init_path / "__init__.py"
    # check if init.py exists
    if not init_file_path.exists():
        with open(init_file_path, "w") as f:
            f.write("")

    console.print("[bold green]auth init setup generated successfully![/bold green]")
