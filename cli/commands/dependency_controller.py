from pathlib import Path

import typer
from rich.console import Console

app = typer.Typer(help="Generate controller dependency setup for FastAPI project")
console = Console()


@app.command()
def dependency_controller(
        name: str = typer.Argument(..., help="Name of the controller"),
        folder: str = typer.Option(None, help="Folder where the controller is located"),
):
    """Generate controller dependency setup for FastAPI project."""

    console.print("[bold green]Generating controller dependency setup...[/bold green]")
    # create controller.py file inside core/dependencies folder

    init_file_path = Path("core") / "__init__.py"
    if not init_file_path.exists():
        init_file_path.write_text("")

    dependency_path = Path("core/dependencies")
    dependency_path.mkdir(parents=True, exist_ok=True)

    init_file_path = dependency_path / "__init__.py"
    if not init_file_path.exists():
        init_file_path.write_text("")

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
        
    controller_dependency_file_path = dependency_path / f"{name.lower()}_controller.py"

    with open(controller_dependency_file_path, "w") as f:
        f.write(f'''from fastapi import Depends

from apps.{name.lower()}.services.{name.lower()} import {name.title().replace("_", "")}Service
from apps.{name.lower()}.controllers.{name.lower()} import {name.title().replace("_", "")}Controller
from core.dependencies.{"" if not folder else f"{folder}."}{name.lower()}_service import {name.lower()}_service_dep

def {name.lower()}_controller_dep(service: {name.title().replace("_", "")}Service = Depends({name.lower()}_service_dep)) -> {name.title().replace("_", "")}Controller:
    return {name.title().replace("_", "")}Controller(service)

''')

    dependency_file_path = Path("core/dependencies") / "__init__.py"
    # check if init.py exists
    if not dependency_file_path.exists():
        with open(dependency_file_path, "w") as f:
            f.write("")
    # check if get_controller import already exists inside init.py
    import_statement = f"from .{"" if not folder else f"{folder}."}{name.lower()}_controller import {name.lower()}_controller_dep\n"
    with open(dependency_file_path, "r") as f:
        content = f.readlines()
        # add import statement if not exists
        if import_statement not in content:
            content.insert(0, import_statement)

            # order imports alphabetically
            content.sort()
            with open(dependency_file_path, "w") as f:
                f.writelines(content)

    console.print("[bold green]controller dependency setup generated successfully![/bold green]")
