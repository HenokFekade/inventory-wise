import os
import typer
from rich.console import Console

console = Console()
app = typer.Typer(help="Generate gitignore files")

@app.command()
def make_gitignore():
    file = ".gitignore"
    if os.path.exists(file):
        console.print(f"[yellow]⚠️ gitignore file already exists![/yellow]")
        raise typer.Exit()
    with open(file, "w") as f:
        f.write(
            "# Python\n*.pyc\n*.pyo\n*.pyd\n__pycache__/\n*.env\n\n"
            "# Virtual Environment\nvenv/\nenv/\n.venv/\n\n"
            "# IDEs and Editors\n.vscode/\n.idea/\n*.swp\n\n"
            "# Logs\n*.log\nlogs/\n\n"
            "# OS-specific\n.DS_Store\nThumbs.db\n\n"
            "# FastAPI-specific\ninstance/\n*.db\n*.sqlite3\n\n"
            "# Docker\ndocker-compose.override.yml\n*.dockerignore\n\n"
            "# Testing\n.coverage\nhtmlcov/\n.tox/\n.nox/\n.pytest_cache/\n.cache/\n\n"
            "# Build\nbuild/\ndist/\n*.egg-info/\n\n"
        )
    console.print(f"[green]✅ gitignore file created successfully.![/green]")
