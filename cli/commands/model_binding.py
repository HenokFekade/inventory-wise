from pathlib import Path

import typer
from rich.console import Console

app = typer.Typer(help="Generate model binding setup for FastAPI project")
console = Console()


@app.command()
def model_binding(
        name: str = typer.Argument(..., help="Name of the model"),
        folder: str = typer.Option(None, help="Folder where the model is located"),
):
    """Generate model binding setup for FastAPI project."""

    console.print("[bold green]Generating model binding setup...[/bold green]")
    # create model.py file inside core/dependencies folder

    init_file_path = Path("core") / "__init__.py"
    if not init_file_path.exists():
        init_file_path.write_text("")

    binding_path = Path("core/dependencies")
    binding_path.mkdir(parents=True, exist_ok=True)

    init_file_path = binding_path / "__init__.py"
    if not init_file_path.exists():
        init_file_path.write_text("")

    # create __init__.py file inside core/dependencies folder
    init_file_path = binding_path / "__init__.py"
    if not init_file_path.exists():
        with open(init_file_path, "w") as f:
            f.write("")

    if folder:
        folder_path = binding_path / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        init_file_path = folder_path / "__init__.py"
        if not init_file_path.exists():
            init_file_path.write_text("")
        binding_path = folder_path

    model_binding_file_path = binding_path / f"{name.lower()}_binding.py"

    with open(model_binding_file_path, "w") as f:
        f.write(f'''from typing import Type
from uuid import UUID

from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from apps.{name.lower()}.models.{name.lower()} import {name.title().replace("_", "")}Model
from exceptions.not_found import NotFoundException
from core.dependencies.db import db_dep

async def {name.lower()}_model_binding(_id: UUID = Path(alias="id"), db: AsyncSession = Depends(db_dep)) -> Type[{name.title().replace("_", "")}Model]:
    instance = await db.get({name.title().replace("_", "")}Model, _id)
    if not instance:
        NotFoundException.throw(f"{name.replace('_', ' ')} not found")
    return instance

''')

    binding_file_path = Path("core/dependencies") / "__init__.py"
    # check if init.py exists
    if not binding_file_path.exists():
        with open(binding_file_path, "w") as f:
            f.write("")
    # check if get_model import already exists inside init.py
    import_statement = f"from .{"" if not folder else f"{folder}."}{name.lower()}_binding import {name.lower()}_model_binding\n"
    with open(binding_file_path, "r") as f:
        content = f.readlines()
        # add import statement if not exists
        if import_statement not in content:
            content.insert(0, import_statement)

            # order imports alphabetically
            content.sort()
            with open(binding_file_path, "w") as f:
                f.writelines(content)

    console.print("[bold green]model binding setup generated successfully![/bold green]")
