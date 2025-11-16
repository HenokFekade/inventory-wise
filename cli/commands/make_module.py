from pathlib import Path

import typer
from commands.make_controller import make_controller
from commands.make_model import make_model
from commands.make_repo import make_repository
from commands.make_route import make_route
from commands.make_schema import make_schema
from commands.make_service import make_service
from commands.dependency_controller import dependency_controller
from commands.dependency_repo import dependency_repo
from commands.dependency_service import dependency_service
from commands.dependency_validator import dependency_validator
from commands.model_binding import model_binding
from rich.console import Console

console = Console()
app = typer.Typer(help="Generate module files")

@app.command()
def make_module(
    name: str = typer.Argument(..., help="Name of the module"),
    resource: bool = typer.Option(False, "-r", "--resource", help="Create a resourceful module with controller")
):
    """Create a new module (optionally with controller using -r flag)."""

    init_file_path = Path("apps") / "__init__.py"
    if not init_file_path.exists():
        init_file_path.write_text("")
        
    modules_path = Path(f"apps/{name}")
    modules_path.mkdir(parents=True, exist_ok=True)

    init_file_path = modules_path / "__init__.py"
    if not init_file_path.exists():
        init_file_path.write_text("")

    # If -r flag passed, also create a controller
    if resource:
        make_model(name=name, resource=True)
        make_controller(name=name, resource=True)
        make_repository(name=name, resource=True)
        make_service(name=name, resource=True)
        make_schema(name=name, resource=True)
        make_route(name=name, resource=True)
        dependency_controller(name=name, folder=name)
        dependency_repo(name=name, folder=name)
        dependency_service(name=name, folder=name)
        dependency_validator(name=f"create_{name.lower()}", folder=name,
                             schema=f"Create{name.title().replace('_', '')}Schema")
        dependency_validator(name=f"update_{name.lower()}", folder=name,
                             schema=f"Update{name.title().replace('_', '')}Schema")
        model_binding(name=name, folder=name)

    console.print(f"[green]✅ Module '{name}' created at {modules_path}![/green]")