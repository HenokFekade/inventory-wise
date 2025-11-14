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

    file_path.write_text(service_template)
    console.print(f"[green]✅ service '{name}' created at {file_path}![/green]")

    # If -r flag passed, also create a service
    if resource:
        console.print("[cyan]Generating resource service...[/cyan]")
