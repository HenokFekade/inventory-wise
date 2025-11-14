import os
import subprocess
from typing import List
from rich.console import Console

from utils.get_venv_python import get_venv_python

console = Console()

def run_command_on_python(command: List[str]):
    """Install a package into the virtual environment using pip."""
    venv_python = str(get_venv_python())
    console.print(f"[cyan]Running command: {' '.join(command)}[/cyan]")
    if os.path.exists(venv_python):
        try:
            subprocess.run([venv_python, "-m"] + command, check=True, text=True)
        except subprocess.CalledProcessError as e:
            console.print(f"[red]Error: Failed to run command {' '.join(command)}. {e}[/red]")
            return
        console.print(f"[green]Command {' '.join(command)} ran successfully.[/green]")
    else:
        console.print(f"[red]Error: Virtual environment Python '{venv_python}' not found.[/red]")