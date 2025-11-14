import typer
from rich.console import Console
from pathlib import Path

console = Console()
app = typer.Typer(help="Generate schema util files")

@app.command()
def make_schema_util():
    """Create a new schema util (optionally with controller using -r flag)."""
    
    schema_utils_path = Path("utils/schemas")
    schema_utils_path.mkdir(parents=True, exist_ok=True)
    file_path = schema_utils_path / f"base_schema.py"

    # Check if schema util already exists
    if file_path.exists():
        console.print(f"[yellow]⚠️ Model 'base_schema' already exists![/yellow]")
        raise typer.Exit()

    # Create basic schema util template
    schema_util_template = f"""from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class DatabaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class BaseSchema(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class BaseResponseSchema(BaseModel):
    message: str
    status: int


class BasePaginationResponseSchema(BaseModel):
    message: str
    status: int
    total: int
    page: int
    per_page: int


"""


    file_path.write_text(schema_util_template)
    console.print(f"[green]✅ Util 'base schema' created at {file_path}![/green]")
