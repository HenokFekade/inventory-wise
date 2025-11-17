from pathlib import Path

import typer
from rich.console import Console

console = Console()
app = typer.Typer(help="Generate model files")

@app.command()
def make_model(
    name: str = typer.Argument(..., help="Name of the model"),
    resource: bool = typer.Option(False, "-r", "--resource", help="Create a resourceful model with controller")
):
    """Create a new model (optionally with controller using -r flag)."""

    init_file_path = Path("apps") / "__init__.py"
    if not init_file_path.exists():
        init_file_path.write_text("")
        
    models_path = Path(f"apps/{name.lower()}/models")
    models_path.mkdir(parents=True, exist_ok=True)

    init_file_path = models_path / "__init__.py"
    if not init_file_path.exists():
        init_file_path.write_text("")
    
    file_path = models_path / f"{name.lower()}.py"

    init_file_path = models_path / "__init__.py"
    if not init_file_path.exists():
        init_file_path.write_text("")

    # Check if model already exists
    if file_path.exists():
        console.print(f"[yellow]⚠️ Model '{name}' already exists![/yellow]")
        raise typer.Exit()

    # Create basic model template
    model_template = f"""from uuid import uuid4

from sqlalchemy import Column, UUID

from connections.database import BaseDatabase
from utils.models.base_model import TimestampMixin

            
             
class {name.title().replace("_", "").replace("Model", "")}Model(TimestampMixin, BaseDatabase):
    __tablename__ = "{name.lower()}s"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
"""

    file_path.write_text(model_template)
    console.print(f"[green]✅ Model '{name}' created at {file_path}![/green]")

    # If -r flag passed, also create a controller
    if resource:
        console.print("[cyan]Generating resource controller...[/cyan]")
