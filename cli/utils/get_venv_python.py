import os
from pathlib import Path


def get_venv_python() -> Path:
    if os.path.exists(".venv"):
        venv_dir = Path(".venv")
    elif os.path.exists("venv"):
        venv_dir = Path("venv")
    else:
        raise FileNotFoundError("No virtual environment directory found (.venv or venv).")
    
    """Return the path to the venv's Python executable."""
    if os.name == "nt":
        return venv_dir / "Scripts" / "python.exe"
    else:
        return venv_dir / "bin" / "python"