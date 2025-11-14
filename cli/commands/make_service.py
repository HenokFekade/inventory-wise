import typer
from rich.console import Console
from pathlib import Path

console = Console()
app = typer.Typer(help="Generate service files")

@app.command()
def make_service(
    name: str = typer.Argument(..., help="Name of the service"),
    resource: bool = typer.Option(False, "-r", "--resource", help="Create a resourceful service with service")
):
    """Create a new service (optionally with service using -r flag)."""
    
    services_path = Path(f"apps/{name.lower()}/services")
    services_path.mkdir(parents=True, exist_ok=True)
    file_path = services_path / f"{name.lower()}.py"

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

    file_path.write_text(service_template)
    console.print(f"[green]✅ service '{name}' created at {file_path}![/green]")

    # If -r flag passed, also create a service
    if resource:
        console.print("[cyan]Generating resource service...[/cyan]")
