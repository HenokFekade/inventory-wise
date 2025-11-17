from pathlib import Path

import typer
from rich.console import Console

console = Console()
app = typer.Typer(help="Generate repository files")

@app.command()
def make_repository(
    name: str = typer.Argument(..., help="Name of the repository"),
    resource: bool = typer.Option(False, "-r", "--resource", help="Create a resourceful repository with repository")
):
    """Create a new repository (optionally with repository using -r flag)."""

    init_file_path = Path("apps") / "__init__.py"
    if not init_file_path.exists():
        init_file_path.write_text("")
        
    repositories_path = Path(f"apps/{name.lower()}/repositories")
    repositories_path.mkdir(parents=True, exist_ok=True)

    init_file_path = repositories_path / "__init__.py"
    if not init_file_path.exists():
        init_file_path.write_text("")

    file_path = repositories_path / f"{name.lower()}.py"

    init_file_path = repositories_path / "__init__.py"
    if not init_file_path.exists():
        init_file_path.write_text("")

    # Check if repository already exists
    if file_path.exists():
        console.print(f"[yellow]⚠️ repository '{name}' already exists![/yellow]")
        raise typer.Exit()

    # Create basic repository template
    repository_template = f"""from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.{name.lower()}.models.{name.lower()} import {name.title().replace("_", "")}Model

class {name.title().replace("_", "")}Repository:
    def __init__(self, session: AsyncSession):
        self._session = session

    # Optimized query methods
    @staticmethod
    def _base_query():
        return select({name.title().replace("_", "")}Model)

"""

    if resource:
        repository_template = f"""from typing import Optional, List, Tuple
from uuid import UUID

from sqlalchemy import select, func, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from apps.{name.lower()}.models.{name.lower()} import {name.title().replace("_", "")}Model
from apps.{name.lower()}.schemas.{name.lower()} import Create{name.title().replace("_", "")}ModelSchema, Update{name.title().replace("_", "")}ModelSchema


class {name.title().replace("_", "")}Repository:
    def __init__(self, session: AsyncSession):
        self._session = session

    # Optimized query methods
    @staticmethod
    def _base_query():
        return select({name.title().replace("_", "")}Model)
        
    async def by_pagination(self, search: str, limit: int, offset: int) -> Tuple[List[{name.title().replace("_", "")}Model], int]:
        query = self._base_query()
        query = query.order_by({name.title().replace("_", "")}Model.created_at.desc())  # type: ignore

        result = await self._session.execute(query.limit(limit).offset((offset - 1) * limit))
        results: List[{name.title().replace("_", "")}Model] = list(result.scalars().all())
        count_query = select(func.count()).select_from(query.subquery())
        total = await self._session.scalar(count_query)
        return results, total

    async def by_id(self, _id: UUID) -> Optional[{name.title().replace("_", "")}Model]:
        query = self._base_query().where({name.title().replace("_", "")}Model.id == _id)  # type: ignore
        return await self._session.scalar(query)

    async def store(self, data: Create{name.title().replace("_", "")}ModelSchema) -> {name.title().replace("_", "")}Model:
        model = {name.title().replace("_", "")}Model(**data.model_dump()) # type: ignore
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return model

    async def update(self, _id: UUID, data: Update{name.title().replace("_", "")}ModelSchema) -> Optional[{name.title().replace("_", "")}Model]:
        values = data.model_dump(exclude_none=True)
        if not values:
            return None

        query = update({name.title().replace("_", "")}Model).filter({name.title().replace("_", "")}Model.id == _id).values(values)  # type: ignore
        rows_updated = await self._session.execute(query)
        await self._session.commit()

        if rows_updated == 0:
            return None

        return await self.by_id(_id)

    async def delete(self, _id: UUID):
        query = delete({name.title().replace("_", "")}Model).where({name.title().replace("_", "")}Model.id == _id) # type: ignore
        await self._session.execute(query)
        await self._session.commit()
"""

    file_path.write_text(repository_template)
    console.print(f"[green]✅ repository '{name}' created at {file_path}![/green]")

    # If -r flag passed, also create a repository
    if resource:
        console.print("[cyan]Generating resource repository...[/cyan]")
