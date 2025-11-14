from pathlib import Path

import typer
from rich.console import Console

app = typer.Typer(help="Generate db dependency setup for FastAPI project")
console = Console()


@app.command()
def dependency_db():
    """Generate db dependency setup for FastAPI project."""

    console.print("[bold green]Generating db dependency setup...[/bold green]")
    # create db.py file inside core/dependencies folder

    init_file_path = Path("core") / "__init__.py"
    if not init_file_path.exists():
        init_file_path.write_text("")

    dependency_path = Path("core/dependencies")
    dependency_path.mkdir(parents=True, exist_ok=True)

    init_file_path = dependency_path / "__init__.py"
    if not init_file_path.exists():
        init_file_path.write_text("")

    dependency_path.mkdir(parents=True, exist_ok=True)
    # create __init__.py file inside core/dependencies folder
    init_file_path = dependency_path / "__init__.py"
    if not init_file_path.exists():
        with open(init_file_path, "w") as f:
            f.write("")
    db_dependency_file_path = dependency_path / "db.py"

    with open(db_dependency_file_path, "w") as f:
        f.write(f'''from connections.database import AsyncSessionLocal

async def db_dep():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()

''')

    dependency_file_path = dependency_path / "__init__.py"
    # check if init.py exists
    if not dependency_file_path.exists():
        with open(dependency_file_path, "w") as f:
            f.write("")

    console.print("[bold green]db dependency setup generated successfully![/bold green]")
