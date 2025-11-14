import os
import subprocess
from rich.console import Console

from utils.get_venv_python import get_venv_python

console = Console()

def install_package(name: str):
    """Install a package into the virtual environment using pip."""
    venv_python = str(get_venv_python())
    console.print(f"[cyan]Installing {name} package...[/cyan]")
    if os.path.exists(venv_python):
        try:
            subprocess.run([venv_python, "-m", "pip", "install", name], check=True, text=True)
        except subprocess.CalledProcessError as e:
            console.print(f"[red]Error: Failed to install {name} package. {e}[/red]")
            return
        console.print(f"[green]{name} package installed successfully.[/green]")
    else:
        console.print(f"[red]Error: Virtual environment Python '{venv_python}' not found.[/red]")