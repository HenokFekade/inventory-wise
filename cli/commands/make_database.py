from pathlib import Path

import typer
from rich.console import Console
from utils.install_package import install_package

app = typer.Typer(help="Generate database setup for FastAPI project")
console = Console()

@app.command()
def make_database():
    """Generate database setup for FastAPI project."""
    
    console.print("[bold green]Generating database setup...[/bold green]")
    
    # install SQLAlchemy package
    install_package("SQLAlchemy")
    install_package("asyncpg")
    
    # create database.py inside connections folder
    connections_path = Path("connections")

    init_file_path = Path("connections") / "__init__.py"
    if not init_file_path.exists():
        init_file_path.write_text("")
        
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