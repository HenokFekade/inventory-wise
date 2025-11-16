from pathlib import Path

import typer
from rich.console import Console

console = Console()
app = typer.Typer(help="Generate route files")


@app.command()
def make_route(
        name: str = typer.Argument(..., help="Name of the route"),
        resource: bool = typer.Option(False, "-r", "--resource", help="Create a resourceful route with route")
):
    """Create a new route (optionally with route using -r flag)."""

    init_file_path = Path("apps") / "__init__.py"
    if not init_file_path.exists():
        init_file_path.write_text("")

    routes_path = Path(f"apps/{name.lower()}/routes")
    routes_path.mkdir(parents=True, exist_ok=True)

    init_file_path = routes_path / "__init__.py"
    if not init_file_path.exists():
        init_file_path.write_text("")

    file_path = routes_path / f"{name.lower()}.py"

    init_file_path = routes_path / "__init__.py"
    if not init_file_path.exists():
        init_file_path.write_text("")

    # Check if route already exists
    if file_path.exists():
        console.print(f"[yellow]⚠️ route '{name}' already exists![/yellow]")
        raise typer.Exit()

    # Create basic route template
    route_template = f"""from fastapi import APIRouter
            
             
{name}_router = APIRouter(prefix="/{name.replace("_", "-")}s", tags=["{name.title().replace("_", "")}"])

"""

    if resource:
        route_template = f"""from typing import Optional

from fastapi import APIRouter, Depends, Query

from apps.{name.lower()}.controllers.{name.lower()} import {name.title().replace("_", "")}Controller
from apps.{name.lower()}.models.{name.lower()} import {name.title().replace("_", "")}Model
from apps.{name.lower()}.schemas.{name.lower()} import {name.title().replace("_", "")}sResponseSchema, {name.title().replace("_", "")}ResponseSchema, Update{name.title().replace("_", "")}Schema, \\
    Create{name.title().replace("_", "")}Schema
from core.authentications.admin import admin_dep
from core.dependencies import {name.lower()}_controller_dep, {name.lower()}_model_binding, create_{name.lower()}_validator_dep, \
    update_{name.lower()}_validator_dep

{name.lower()}_router = APIRouter(prefix="/{name.lower()}s", tags=["{name.title().replace("_", "")}"])


@{name.lower()}_router.get("", response_model={name.title().replace("_", "")}sResponseSchema)
async def index(
        _=Depends(admin_dep),
        page: int = Query(default=1, ge=1),
        per_page: int = Query(default=10, ge=1, alias="per-page"),
        search: Optional[str] = Query(default=""),
        controller: {name.title().replace("_", "")}Controller = Depends({name.lower()}_controller_dep),
):
    return await controller.index(search=search, per_page=per_page, page=page)


@{name.lower()}_router.post("", response_model={name.title().replace("_", "")}ResponseSchema, status_code=201)
async def create_{name.lower()}(
        data: Create{name.title().replace("_", "")}Schema = Depends(create_{name.lower()}_validator_dep),
        controller: {name.title().replace("_", "")}Controller = Depends({name.lower()}_controller_dep),
        _=Depends(admin_dep),
):
    return await controller.store(data=data)


@{name.lower()}_router.get("/{{id}}", response_model={name.title().replace("_", "")}ResponseSchema)
async def get_by_id(
        {name.lower()}: {name.title().replace("_", "")}Model = Depends({name.lower()}_model_binding),
        controller: {name.title().replace("_", "")}Controller = Depends({name.lower()}_controller_dep),
        _=Depends(admin_dep),
):
    return await controller.by_id({name.lower()}={name.lower()})


@{name.lower()}_router.patch("/{{id}}", response_model={name.title().replace("_", "")}ResponseSchema)
async def update(
        {name.lower()}: {name.title().replace("_", "")}Model = Depends({name.lower()}_model_binding),
        data: Update{name.title().replace("_", "")}Schema = Depends(update_{name.lower()}_validator_dep),
        controller: {name.title().replace("_", "")}Controller = Depends({name.lower()}_controller_dep),
        _=Depends(admin_dep),
):
    return await controller.update({name.lower()}={name.lower()}, data=data)


@{name.lower()}_router.delete("/{{id}}", response_model={name.title().replace("_", "")}ResponseSchema)
async def update(
        {name.lower()}: {name.title().replace("_", "")}Model = Depends({name.lower()}_model_binding),
        controller: {name.title().replace("_", "")}Controller = Depends({name.lower()}_controller_dep),
        _=Depends(admin_dep),
):
    return await controller.delete(data={name.lower()})

"""

    file_path.write_text(route_template)
    console.print(f"[green]✅ route '{name}' created at {file_path}![/green]")

    # If -r flag passed, also create a route
    if resource:
        console.print("[cyan]Generating resource route...[/cyan]")
