import subprocess
import sys

from rich.console import Console


console = Console()

def run_command_line(command):
    """
    Executes a command in a subprocess.
    """
    try:
        # Run the command. capture_output=False lets the command's output
        # go directly to the console if it prints anything.
        # If you wanted to capture and process output, set capture_output=True
        # and handle stdout/stderr from the result object.
        result = subprocess.run(
            command,
            check=True, # Raise CalledProcessError if the command returns a non-zero exit code
            shell=True, # Use shell for command execution (e.g., to handle pipes, environment setup)
            # You might want to adjust shell=True based on your command complexity and security needs.
            # For 'python -m venv', often shell=False and a list for 'command' is safer/better practice:
            # e.g., command=['python', '-m', 'venv', 'my_env']
        )
        return result
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error: Command '{' '.join(e.cmd)}' failed with exit code {e.returncode}.[/red]")
        # If capture_output was True, you could print e.stdout and e.stderr here.
        raise # Re-raise the exception after cleaning up the loader
    except Exception as e:
        console.print(f"[red]An unexpected error occurred: {e}[/red]")
        raise
