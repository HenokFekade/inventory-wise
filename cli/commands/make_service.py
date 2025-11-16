from pathlib import Path

import typer
from rich.console import Console

console = Console()
app = typer.Typer(help="Generate service files")

@app.command()
def make_service(
    name: str = typer.Argument(..., help="Name of the service"),
    resource: bool = typer.Option(False, "-r", "--resource", help="Create a resourceful service with service")
):
    """Create a new service (optionally with service using -r flag)."""

    init_file_path = Path("apps") / "__init__.py"
    if not init_file_path.exists():
        init_file_path.write_text("")
        
    services_path = Path(f"apps/{name.lower()}/services")
    services_path.mkdir(parents=True, exist_ok=True)

    init_file_path = services_path / "__init__.py"
    if not init_file_path.exists():
        init_file_path.write_text("")

    file_path = services_path / f"{name.lower()}.py"

    init_file_path = services_path / "__init__.py"
    if not init_file_path.exists():
        init_file_path.write_text("")

    # Check if service already exists
    if file_path.exists():
        console.print(f"[yellow]⚠️ service '{name}' already exists![/yellow]")
        raise typer.Exit()

    # Create basic service template
    service_template = f"""from apps.{name}.repositories.{name.lower()} import {name.title().replace("_", "")}Repository
            
            
class {name.title().replace("_", "")}Service:
    def __init__(self, repo: {name.title().replace("_", "")}Repository):
        self._repo = repo

"""

    if resource:
        service_template = f"""from apps.{name.lower()}.models.{name.lower()} import {name.title().replace("_", "")}Model
from apps.{name.lower()}.repositories.{name.lower()} import {name.title().replace("_", "")}Repository
from apps.{name.lower()}.schemas.{name.lower()} import {name.title().replace("_", "")}sResponseSchema, {name.title().replace("_", "")}Schema, {name.title().replace("_", "")}ResponseSchema, \\
    Create{name.title().replace("_", "")}Schema, Create{name.title().replace("_", "")}ModelSchema, Update{name.title().replace("_", "")}Schema, Update{name.title().replace("_", "")}ModelSchema


class {name.title().replace("_", "")}Service:
    def __init__(self, repo: {name.title().replace("_", "")}Repository):
        self._repo = repo

    
    async def index(self, search: str, per_page: int, page: int) -> {name.title().replace("_", "")}sResponseSchema:
        result, total = await self._repo.by_pagination(offset=page, search=search, limit=per_page)
        data = [{name.title().replace("_", "")}Schema.model_validate(value) for value in result]
        return {name.title().replace("_", "")}sResponseSchema(data=data, total=total, page=page, per_page=per_page)

    @staticmethod
    async def by_id(data: {name.title().replace("_", "")}Model) -> {name.title().replace("_", "")}ResponseSchema:
        return {name.title().replace("_", "")}ResponseSchema(data={name.title().replace("_", "")}Schema.model_validate(data))

    async def store(self, data: Create{name.title().replace("_", "")}Schema) -> {name.title().replace("_", "")}ResponseSchema:
        data = await self._repo.store(Create{name.title().replace("_", "")}ModelSchema(**data.model_dump()))
        return {name.title().replace("_", "")}ResponseSchema(
            data={name.title().replace("_", "")}Schema.model_validate(data),
            status=201,
            message="{name.title().replace("_", "")} created successfully",
        )

    async def update(self, {name.lower()}: {name.title().replace("_", "")}Model, data: Update{name.title().replace("_", "")}Schema) -> {name.title().replace("_", "")}ResponseSchema:
        data = Update{name.title().replace("_", "")}ModelSchema(**data.model_dump())
        result = await self._repo.update(data=data, _id={name.lower()}.id)
        return {name.title().replace("_", "")}ResponseSchema(
            data={name.title().replace("_", "")}Schema.model_validate(result),
            message="{name.title().replace("_", "")} updated successfully",
        )

    async def delete(self, data: {name.title().replace("_", "")}Model) -> {name.title().replace("_", "")}ResponseSchema:
        await self._repo.delete(_id=data.id)
        return {name.title().replace("_", "")}ResponseSchema(
            data={name.title().replace("_", "")}Schema.model_validate(data),
            message="{name.title().replace("_", "")} deleted successfully",
        )

"""

    file_path.write_text(service_template)
    console.print(f"[green]✅ service '{name}' created at {file_path}![/green]")

    # If -r flag passed, also create a service
    if resource:
        console.print("[cyan]Generating resource service...[/cyan]")
