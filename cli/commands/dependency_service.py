from pathlib import Path

import typer
from rich.console import Console

app = typer.Typer(help="Generate service dependency setup for FastAPI project")
console = Console()


@app.command()
def dependency_service(
        name: str = typer.Argument(..., help="Name of the service"),
):
    """Generate service dependency setup for FastAPI project."""

    console.print("[bold green]Generating service dependency setup...[/bold green]")
    # create service.py file inside core/dependencies folder

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
    service_dependency_file_path = dependency_path / f"{name.lower()}_service.py"

    with open(service_dependency_file_path, "w") as f:
        f.write(f'''from fastapi import Depends

from apps.{name.lower()}.repositories.{name.lower()} import {name.title().replace("_", "")}Repository
from apps.{name.lower()}.services.{name.lower()} import {name.title().replace("_", "")}Service
from core.dependencies.{name.lower()}_repo import {name.lower()}_repo_dep

def {name.lower()}_service_dep(repo: {name.title().replace("_", "")}Repository = Depends({name.lower()}_repo_dep)) -> {name.title().replace("_", "")}Service:
    return {name.title().replace("_", "")}Service(repo)

''')

    dependency_file_path = dependency_path / "__init__.py"
    # check if init.py exists
    if not dependency_file_path.exists():
        with open(dependency_file_path, "w") as f:
            f.write("")

    console.print("[bold green]service dependency setup generated successfully![/bold green]")
