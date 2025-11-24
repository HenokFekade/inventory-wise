from pathlib import Path

import typer
from rich.console import Console

console = Console()
app = typer.Typer(help="Generate controller files")

@app.command()
def make_controller(
    name: str = typer.Argument(..., help="Name of the controller"),
    resource: bool = typer.Option(False, "-r", "--resource", help="Create a resourceful controller with controller")
):
    """Create a new controller (optionally with controller using -r flag)."""

    init_file_path = Path("apps") / "__init__.py"
    if not init_file_path.exists():
        init_file_path.write_text("")
        
    controllers_path = Path(f"apps/{name.lower()}/controllers")
    controllers_path.mkdir(parents=True, exist_ok=True)

    init_file_path = controllers_path / "__init__.py"
    if not init_file_path.exists():
        init_file_path.write_text("")
    
    file_path = controllers_path / f"{name.lower()}.py"

    init_file_path = controllers_path / "__init__.py"
    if not init_file_path.exists():
        init_file_path.write_text("")

    # Check if controller already exists
    if file_path.exists():
        console.print(f"[yellow]⚠️ controller '{name}' already exists![/yellow]")
        raise typer.Exit()

    # Create basic controller template
    controller_template = f"""from apps.{name.lower()}.services.{name.lower()} import {name.title().replace("_", "")}Service
            
            
class {name.title().replace("_", "")}Controller:
    def __init__(self, service: {name.title().replace("_", "")}Service):
        self._service = service

"""

    if resource:
        controller_template = f"""from apps.{name.lower()}.models.{name.lower()} import {name.title().replace("_", "")}Model
from apps.{name.lower()}.schemas.{name.lower()} import {name.title().replace("_", "")}sResponseSchema, {name.title().replace("_", "")}ResponseSchema, Create{name.title().replace("_", "")}Schema, \\
    Update{name.title().replace("_", "")}Schema
from apps.{name.lower()}.services.{name.lower()} import {name.title().replace("_", "")}Service


class {name.title().replace("_", "")}Controller:
    def __init__(self, service: {name.title().replace("_", "")}Service):
        self._service = service

    async def index(self, search: str, per_page: int, page: int) -> {name.title().replace("_", "")}sResponseSchema:
        return await self._service.index(search=search, per_page=per_page, page=page)

    def by_id(self, {name.lower()}: {name.title().replace("_", "")}Model) -> {name.title().replace("_", "")}ResponseSchema:
        return self._service.by_id(data={name.lower()})

    async def store(self, data: Create{name.title().replace("_", "")}Schema) -> {name.title().replace("_", "")}ResponseSchema:

        return await self._service.store(data)

    async def update(self, {name.lower()}: {name.title().replace("_", "")}Model, data: Update{name.title().replace("_", "")}Schema) -> {name.title().replace("_", "")}ResponseSchema:
        return await self._service.update(data=data, {name.lower()}={name.lower()})
    
    async def delete(self, data: {name.title().replace("_", "")}Model) -> {name.title().replace("_", "")}ResponseSchema:
        return await self._service.delete(data)
"""

    file_path.write_text(controller_template)
    console.print(f"[green]✅ controller '{name}' created at {file_path}![/green]")

    # If -r flag passed, also create a controller
    if resource:
        console.print("[cyan]Generating resource controller...[/cyan]")
