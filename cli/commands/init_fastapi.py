import os
from pathlib import Path

from rich.console import Console
import typer

from utils.run_command_on_python import run_command_on_python
from commands.make_virtual_environment import make_virtual_environment
from commands.install_fastapi import install_fastapi
from commands.make_gitignore import make_gitignore

app = typer.Typer(help="Initialize a FastAPI project")
console = Console()

@app.command()
def init_fastapi(
    name: str = typer.Argument(..., help="Name of the FastAPI project"),
):
    """Initialize a basic FastAPI project structure."""
    
    console.print("[bold green]Initializing FastAPI project...[/bold green]")
    
    make_virtual_environment()
    install_fastapi()
    make_gitignore()
    
    # create main.py
    console.print("[bold green]Creating main.py...[/bold green]")
    with open("main.py", "w") as f:
        f.write(f'''from fastapi import FastAPI

# initialize server
app = FastAPI(lifespan=lifespan, title="{name} API")

@app.get("/health")
def health():
    return {
        "status": 200,
        "message": f"{name} API Server is running successfully",
    }
''')
        
    # create requirements.txt
    console.print("[bold green]Creating requirements.txt...[/bold green]")
    with open("requirements.txt", "w") as f:
        run_command_on_python(["pip", "freeze", ">", "requirements.txt"])
        

    console.print("[bold green]FastAPI project initialized successfully![/bold green]")