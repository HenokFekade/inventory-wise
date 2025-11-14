from pathlib import Path

import typer
from rich.console import Console

app = typer.Typer(help="Generate make exception setup for FastAPI project")
console = Console()


@app.command()
def make_exception(
        name: str = typer.Argument(..., help="Name of the exception"),
        status: int = typer.Option(..., help="HTTP status code for the exception"),
):
    """Generate make exception setup for FastAPI project."""

    console.print("[bold green]Generating make exception setup...[/bold green]")

    exception_path = Path("exceptions")
    exception_path.mkdir(parents=True, exist_ok=True)

    init_file_path = exception_path / "__init__.py"
    if not init_file_path.exists():
        init_file_path.write_text("")

    exception_path.mkdir(parents=True, exist_ok=True)
    # create __init__.py file inside exceptions folder
    init_file_path = exception_path / "__init__.py"
    if not init_file_path.exists():
        with open(init_file_path, "w") as f:
            f.write("")
    make_exception_file_path = exception_path / f"{name.lower()}.py"

    if status == 400:
        status_name = "status.HTTP_400_BAD_REQUEST"
    elif status == 403:
        status_name = "status.HTTP_403_FORBIDDEN"
    elif status == 401:
        status_name = "status.HTTP_401_UNAUTHORIZED"
    else:
        status_name = "status.HTTP_400_BAD_REQUEST"

    with open(make_exception_file_path, "w") as f:
        f.write(f'''from fastapi import HTTPException, status
from starlette.responses import JSONResponse


class {name.title().replace("_", "")}Exception(HTTPException):
    _status_code = {status_name}

    def __init__(self, message: str = "Bad Request"):
        self.message = message
        super().__init__(status_code=self._status_code, detail=message)

    @classmethod
    def throw(cls, message: str):
        raise cls(message=message)


def {name}_exception_handler(exc: {name.title().replace("_", "")}Exception):
    return JSONResponse(
        status_code=exc.status_code,
        content={{"message": exc.message, "errors": [], "status": exc.status_code}},
    )

''')

    exception_file_path = exception_path / "__init__.py"
    # check if init.py exists
    if not exception_file_path.exists():
        with open(exception_file_path, "w") as f:
            f.write("")

    main_path = Path("main.py")
    if main_path.exists():
        with open(main_path, "r") as f:
            content = f.readlines()

            data = f'''from exceptions.{name} import {name.title().replace("_", "")}Exception, {name}_exception_handler'''
            if data not in content:
                did_internal_import_exist = False
                for index in range(len(content)):
                    if did_internal_import_exist:
                        if data < content[index]:
                            continue
                        else:
                            content.insert(index, f"{data}\n")
                            break
                    else:
                        if content[index].startswith("from apps."):
                            did_internal_import_exist = True
            data = f'''@app.exception_handler({name.title().replace("_", "")}Exception)'''
            if data not in content:
                if "# handle exceptions" in content:
                    content.append(f'''
@app.exception_handler({name.title().replace("_", "")}Exception)
def handle_{name}_exception(_, exc: {name.title().replace("_", "")}Exception):
    return {name}_exception_handler(exc=exc)

    ''')
                else:
                    content.append(f'''# handle exceptions
@app.exception_handler({name.title().replace("_", "")}Exception)
def handle_{name}_exception(_, exc: {name.title().replace("_", "")}Exception):
    return {name}_exception_handler(exc=exc)

    ''')
                with open(main_path, "w") as f:
                    f.writelines(content)

    console.print("[bold green]make exception setup generated successfully![/bold green]")
