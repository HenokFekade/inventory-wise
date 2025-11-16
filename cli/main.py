import typer
from rich.console import Console

from commands.auth_init import auth_init
from commands.dependency_controller import dependency_controller
from commands.dependency_db import dependency_db
from commands.dependency_repo import dependency_repo
from commands.dependency_service import dependency_service
from commands.dependency_validator import dependency_validator
from commands.init_fastapi import init_fastapi
from commands.install_fastapi import install_fastapi
from commands.make_auth import make_auth
from commands.make_config import make_config
from commands.make_controller import make_controller
from commands.make_database import make_database
from commands.make_exception import make_exception
from commands.make_gitignore import make_gitignore
from commands.make_model import make_model
from commands.make_model_util import make_model_util
from commands.make_module import make_module
from commands.make_repo import make_repository
from commands.make_route import make_route
from commands.make_schema import make_schema
from commands.make_schema_util import make_schema_util
from commands.make_service import make_service
from commands.make_virtual_environment import make_virtual_environment
from commands.model_binding import model_binding

app = typer.Typer(help="A CLI tool for FASTAPI applications. Inspired by Laravel's Artisan.")
console = Console()

# Register commands directly
app.command("model:binding")(model_binding)
app.command("make:model:util")(make_model_util)
app.command("make:schema:util")(make_schema_util)
app.command("make:exception")(make_exception)
app.command("auth:init")(auth_init)
app.command("make:auth")(make_auth)
app.command("dependency:db")(dependency_db)
app.command("dependency:repo")(dependency_repo)
app.command("dependency:validator")(dependency_validator)
app.command("make:route")(make_route)
app.command("make:module")(make_module)
app.command("make:model")(make_model)
app.command("make:schema")(make_schema)
app.command("make:controller")(make_controller)
app.command("make:service")(make_service)
app.command("make:repo")(make_repository)
app.command("make:venv")(make_virtual_environment)
app.command("make:gitignore")(make_gitignore)
app.command("install:fastapi")(install_fastapi)
app.command("init:fastapi")(init_fastapi)
app.command("make:config")(make_config)
app.command("make:database")(make_database)
app.command("dependency:service")(dependency_service)
app.command("dependency:controller")(dependency_controller)

if __name__ == "__main__":
    app()