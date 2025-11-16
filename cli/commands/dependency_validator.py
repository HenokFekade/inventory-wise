from pathlib import Path

import typer
from rich.console import Console

app = typer.Typer(help="Generate validator dependency setup for FastAPI project")
console = Console()


@app.command()
def dependency_validator(
        name: str = typer.Argument(..., help="Name of the validator"),
        folder: str = typer.Option(None, help="Folder where the validator is located"),
        schema: str = typer.Option(None, help="Schema Name where the validator will receive"),
):
    """Generate validator dependency setup for FastAPI project."""

    console.print("[bold green]Generating validator dependency setup...[/bold green]")
    # create validator.py file inside core/dependencies folder

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

    if folder:
        folder_path = dependency_path / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        init_file_path = folder_path / "__init__.py"
        if not init_file_path.exists():
            init_file_path.write_text("")
        dependency_path = folder_path

    validator_dependency_file_path = dependency_path / f"{name.lower()}_validator.py"

    with open(validator_dependency_file_path, "w") as f:
        f.write(f'''from fastapi import Depends

from apps.{folder.lower()}.repositories.{folder.lower()} import {folder.title().replace("_", "")}Repository
from apps.{folder.lower()}.schemas.{folder.lower()} import {schema}
from core.dependencies.{"" if not folder else f"{folder}."}{folder.lower()}_repo import {folder.lower()}_repo_dep

async def {name.lower()}_validator_dep(
    data: {schema},
    repo: {folder.title().replace("_", "")}Repository = Depends({folder.lower()}_repo_dep),
) -> {schema}:
    return data

''')

    dependency_file_path = dependency_path / "__init__.py"
    # check if init.py exists
    if not dependency_file_path.exists():
        with open(dependency_file_path, "w") as f:
            f.write("")

    dependency_file_path = Path("core/dependencies") / "__init__.py"
    # check if init.py exists
    if not dependency_file_path.exists():
        with open(dependency_file_path, "w") as f:
            f.write("")
    # check if get_validator import already exists inside init.py
    import_statement = f"from .{"" if not folder else f"{folder}."}{name.lower()}_validator import {name.lower()}_validator_dep\n"
    with open(dependency_file_path, "r") as f:
        content = f.readlines()
        # add import statement if not exists
        if import_statement not in content:
            content.insert(0, import_statement)

            # order imports alphabetically
            content.sort()
            with open(dependency_file_path, "w") as f:
                f.writelines(content)

    console.print("[bold green]validator dependency setup generated successfully![/bold green]")
