import typer

from utils.install_package import install_package


app = typer.Typer(help="Install FastAPI package")

@app.command()
def install_fastapi():
    install_package('"fastapi[standard]"')
