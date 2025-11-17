from pathlib import Path

import typer
from rich.console import Console

console = Console()
app = typer.Typer(help="Generate schema files")

@app.command()
def make_schema(
    name: str = typer.Argument(..., help="Name of the schema"),
    resource: bool = typer.Option(False, "-r", "--resource", help="Create a resourceful schema with controller")
):
    """Create a new schema (optionally with controller using -r flag)."""

    init_file_path = Path("apps") / "__init__.py"
    if not init_file_path.exists():
        init_file_path.write_text("")
          
    schemas_path = Path(f"apps/{name.lower()}/schemas")
    schemas_path.mkdir(parents=True, exist_ok=True)

    init_file_path = schemas_path / "__init__.py"
    if not init_file_path.exists():
        init_file_path.write_text("")
        
    file_path = schemas_path / f"{name.lower()}.py"

    init_file_path = schemas_path / "__init__.py"
    if not init_file_path.exists():
        init_file_path.write_text("")

    # Check if schema already exists
    if file_path.exists():
        console.print(f"[yellow]⚠️ Model '{name}' already exists![/yellow]")
        raise typer.Exit()

    # Create basic schema template
    schema_template = f"""from pydantic import BaseModel

"""

    if resource:
        schema_template = f"""
from typing import Optional, List

from pydantic import BaseModel

from utils.schemas.base_schema import BaseSchema, BaseResponseSchema, BasePaginationResponseSchema


class Create{name.title().replace("_", "")}Schema(BaseModel):
    pass

class Create{name.title().replace("_", "")}ModelSchema(Create{name.title().replace("_", "")}Schema):
    pass

class Update{name.title().replace("_", "")}Schema(BaseModel):
    pass

class Update{name.title().replace("_", "")}ModelSchema(Update{name.title().replace("_", "")}Schema):
    pass

class {name.title().replace("_", "")}Schema(BaseSchema):
    pass

class {name.title().replace("_", "")}ResponseSchema(BaseResponseSchema):
    data: {name.title().replace("_", "")}Schema
    status: int = 200
    message: str = "{name.title().replace("_", "")} fetched successfully"

class {name.title().replace("_", "")}sResponseSchema(BasePaginationResponseSchema):
    data: List[{name.title().replace("_", "")}Schema]
    status: int = 200
    message: str = "{name.title().replace("_", "")}s fetched successfully"

    """

    file_path.write_text(schema_template)
    console.print(f"[green]✅ Model '{name}' created at {file_path}![/green]")

    # If -r flag passed, also create a controller
    if resource:
        console.print("[cyan]Generating resource controller...[/cyan]")
