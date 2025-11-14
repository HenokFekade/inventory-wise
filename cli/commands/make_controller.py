import typer
from rich.console import Console
from pathlib import Path

console = Console()
app = typer.Typer(help="Generate controller files")

@app.command()
def make_controller(
    name: str = typer.Argument(..., help="Name of the controller"),
    resource: bool = typer.Option(False, "-r", "--resource", help="Create a resourceful controller with controller")
):
    """Create a new controller (optionally with controller using -r flag)."""
    
    controllers_path = Path(f"apps/{name.lower()}/controllers")
    controllers_path.mkdir(parents=True, exist_ok=True)
    file_path = controllers_path / f"{name.lower()}.py"

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

    file_path.write_text(controller_template)
    console.print(f"[green]✅ controller '{name}' created at {file_path}![/green]")

    # If -r flag passed, also create a controller
    if resource:
        console.print("[cyan]Generating resource controller...[/cyan]")
