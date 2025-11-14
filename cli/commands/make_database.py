import os
from pathlib import Path

from rich.console import Console
import typer

from utils.run_command_on_python import run_command_on_python
from utils.install_package import install_package
from commands.make_virtual_environment import make_virtual_environment
from commands.install_fastapi import install_fastapi
from commands.make_gitignore import make_gitignore

app = typer.Typer(help="Generate database setup for FastAPI project")
console = Console()

@app.command()
def make_database():
    """Generate database setup for FastAPI project."""
    
    console.print("[bold green]Generating database setup...[/bold green]")
    
    # install SQLAlchemy package
    install_package("SQLAlchemy")
    
    # create database.py inside connections folder
    connections_path = Path("connections")
    connections_path.mkdir(parents=True, exist_ok=True)
    db_file_path = connections_path / "database.py"
    
    with open(db_file_path, "w") as f:
        f.write(f'''from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from core.config.config import config


engine = create_async_engine(config.DATABASE_URL, pool_size=100, max_overflow=200, pool_timeout=30, pool_recycle=1800)

AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)

BaseDatabase = declarative_base()

''')
    
    console.print("[bold green]Database setup generated successfully![/bold green]")