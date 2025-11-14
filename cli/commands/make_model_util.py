from xml.parsers.expat import model
import typer
from rich.console import Console
from pathlib import Path

console = Console()
app = typer.Typer(help="Generate model util files")

@app.command()
def make_model_util():
    """Create a new model util (optionally with controller using -r flag)."""
    
    model_utils_path = Path("utils/models")
    model_utils_path.mkdir(parents=True, exist_ok=True)
    file_path = model_utils_path / f"base_model.py"

    # Check if model util already exists
    if file_path.exists():
        console.print(f"[yellow]⚠️ Model 'base_model' already exists![/yellow]")
        raise typer.Exit()

    # Create basic model util template
    model_util_template = f"""from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class TimestampMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

"""


    file_path.write_text(model_util_template)
    console.print(f"[green]✅ Util 'base model' created at {file_path}![/green]")
