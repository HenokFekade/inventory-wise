from pathlib import Path

import typer
from rich.console import Console

console = Console()
app = typer.Typer(help="Generate route files")


@app.command()
def make_route(
        name: str = typer.Argument(..., help="Name of the route"),
        resource: bool = typer.Option(False, "-r", "--resource", help="Create a resourceful route with route")
):
    """Create a new route (optionally with route using -r flag)."""

    init_file_path = Path("apps") / "__init__.py"
    if not init_file_path.exists():
        init_file_path.write_text("")

    routes_path = Path(f"apps/{name.lower()}/routes")
    routes_path.mkdir(parents=True, exist_ok=True)

    init_file_path = routes_path / "__init__.py"
    if not init_file_path.exists():
        init_file_path.write_text("")

    file_path = routes_path / f"{name.lower()}.py"

    init_file_path = routes_path / "__init__.py"
    if not init_file_path.exists():
        init_file_path.write_text("")

    # Check if route already exists
    if file_path.exists():
        console.print(f"[yellow]⚠️ route '{name}' already exists![/yellow]")
        raise typer.Exit()

    # Create basic route template
    route_template = f"""from fastapi import APIRouter
            
             
{name}_router = APIRouter(prefix="/{name.replace("_", "-")}s", tags=["{name.title().replace("_", "")}"])

"""

    file_path.write_text(route_template)
    console.print(f"[green]✅ route '{name}' created at {file_path}![/green]")

    # If -r flag passed, also create a route
    if resource:
        console.print("[cyan]Generating resource route...[/cyan]")
