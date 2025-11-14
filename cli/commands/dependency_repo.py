from pathlib import Path

import typer
from rich.console import Console

app = typer.Typer(help="Generate repo dependency setup for FastAPI project")
console = Console()


@app.command()
def dependency_repo(
        name: str = typer.Argument(..., help="Name of the repository"),
):
    """Generate repo dependency setup for FastAPI project."""

    console.print("[bold green]Generating repo dependency setup...[/bold green]")
    # create repo.py file inside core/dependencies folder

    init_file_path = Path("core") / "__init__.py"
    if not init_file_path.exists():
        init_file_path.write_text("")

    dependency_path = Path("core/dependencies")
    dependency_path.mkdir(parents=True, exist_ok=True)

    init_file_path = dependency_path / "__init__.py"
    if not init_file_path.exists():
        init_file_path.write_text("")

    dependency_path.mkdir(parents=True, exist_ok=True)
    # create __init__.py file inside core/dependencies folder
    init_file_path = dependency_path / "__init__.py"
    if not init_file_path.exists():
        with open(init_file_path, "w") as f:
            f.write("")
    repo_dependency_file_path = dependency_path / f"{name.lower()}_repo.py"

    with open(repo_dependency_file_path, "w") as f:
        f.write(f'''from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.{name.lower()}.repositories.{name.lower()} import {name.title().replace("_", "")}Repository
from core.dependencies.db import db_dep

def {name.lower()}_repo_dep(db: AsyncSession = Depends(db_dep)) -> {name.title().replace("_", "")}Repository:
    return {name.title().replace("_", "")}Repository(db)

''')

    dependency_file_path = dependency_path / "__init__.py"
    # check if init.py exists
    if not dependency_file_path.exists():
        with open(dependency_file_path, "w") as f:
            f.write("")

    console.print("[bold green]repo dependency setup generated successfully![/bold green]")
