import os
from typing import Optional
import typer
from rich.console import Console

from utils.run_command_line import run_command_line


console = Console()
app = typer.Typer(help="Generate virtual environment files")

@app.command()
def make_virtual_environment(name: Optional[str] = ".venv"):
    console.print(f"[green]Starting Venv Creation ...[/green]")
    
    # check if folder already exist
    if os.path.exists(name):
        console.print(f"[yellow]⚠️ virtual environment '{name}' already exists![/yellow]")
        raise typer.Exit()
    # On Windows, you might need 'py -m venv' or the full path to python.exe
    # On Unix, 'python3 -m venv' or 'python -m venv'
    run_command_line(["python", "-m", "venv", name])
    console.print(f"[green]✅ Virtual environment '{name}' created successfully.[/green]")
    