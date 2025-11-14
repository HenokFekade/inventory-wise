import typer
from rich.console import Console
from pathlib import Path

console = Console()
app = typer.Typer(help="Generate schema files")

@app.command()
def make_schema(
    name: str = typer.Argument(..., help="Name of the schema"),
    resource: bool = typer.Option(False, "-r", "--resource", help="Create a resourceful schema with controller")
):
    """Create a new schema (optionally with controller using -r flag)."""
    
    schemas_path = Path(f"apps/{name.lower()}/schemas")
    schemas_path.mkdir(parents=True, exist_ok=True)
    file_path = schemas_path / f"{name.lower()}.py"

    # Check if schema already exists
    if file_path.exists():
        console.print(f"[yellow]⚠️ Model '{name}' already exists![/yellow]")
        raise typer.Exit()

    # Create basic schema template
    schema_template = f"""from pydantic import BaseModel

"""

    file_path.write_text(schema_template)
    console.print(f"[green]✅ Model '{name}' created at {file_path}![/green]")

    # If -r flag passed, also create a controller
    if resource:
        console.print("[cyan]Generating resource controller...[/cyan]")
