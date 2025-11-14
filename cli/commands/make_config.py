import os
from pathlib import Path

from rich.console import Console
import typer

from utils.run_command_on_python import run_command_on_python
from utils.install_package import install_package
from commands.make_virtual_environment import make_virtual_environment
from commands.install_fastapi import install_fastapi
from commands.make_gitignore import make_gitignore

app = typer.Typer(help="Generate config setup for FastAPI project")
console = Console()

@app.command()
def make_config():
    """Generate config setup for FastAPI project."""
    
    console.print("[bold green]Generating config setup...[/bold green]")
    install_package("pydantic-settings")
    # create config.py file inside core/config folder
    config_path = Path("core/config")
    config_path.mkdir(parents=True, exist_ok=True)
    config_file_path = config_path / "config.py"
    
    with open(config_file_path, "w") as f:
        f.write(f'''from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    DATABASE_URL: PostgresDsn 

    model_config = SettingsConfigDict(case_sensitive=True, env_file='.env', env_file_encoding='utf-8')

config = Config()

''')
        
    console.print("[bold green]Config setup generated successfully![/bold green]")