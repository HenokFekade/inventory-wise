from pathlib import Path

import typer
from rich.console import Console

console = Console()
app = typer.Typer(help="Generate repository files")

@app.command()
def make_repository(
    name: str = typer.Argument(..., help="Name of the repository"),
    resource: bool = typer.Option(False, "-r", "--resource", help="Create a resourceful repository with repository")
):
    """Create a new repository (optionally with repository using -r flag)."""

    init_file_path = Path("apps") / "__init__.py"
    if not init_file_path.exists():
        init_file_path.write_text("")
        
    repositories_path = Path(f"apps/{name.lower()}/repositories")
    repositories_path.mkdir(parents=True, exist_ok=True)

    init_file_path = repositories_path / "__init__.py"
    if not init_file_path.exists():
        init_file_path.write_text("")

    file_path = repositories_path / f"{name.lower()}.py"

    init_file_path = repositories_path / "__init__.py"
    if not init_file_path.exists():
        init_file_path.write_text("")

    # Check if repository already exists
    if file_path.exists():
        console.print(f"[yellow]⚠️ repository '{name}' already exists![/yellow]")
        raise typer.Exit()

    # Create basic repository template
    repository_template = f"""from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.{name.lower()}.models.{name.lower()} import {name.title().replace("_", "")}Model

class {name.title().replace("_", "")}Repository:
    def __init__(self, session: AsyncSession):
        self._session = session

    # Optimized query methods
    @staticmethod
    def _base_query():
        return select({name.title().replace("_", "")}Model)

"""

    file_path.write_text(repository_template)
    console.print(f"[green]✅ repository '{name}' created at {file_path}![/green]")

    # If -r flag passed, also create a repository
    if resource:
        console.print("[cyan]Generating resource repository...[/cyan]")
