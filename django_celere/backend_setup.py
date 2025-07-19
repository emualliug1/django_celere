import os
import typer
from .utils import run_command

def setup_backend(project_name, choice, linter_formatter_choice, server_choice, pre_commit_choice):
    """Installs backend dependencies using Poetry."""
    
    run_command("poetry init --no-interaction", cwd=project_name)

    common_deps = ["django@latest", "django-vite@latest", "django-widget-tweaks@latest", "python-decouple@latest"]
    run_command(f"poetry add {' '.join(common_deps)} --lock", cwd=project_name)

    if choice == "1":
        run_command("poetry add django-htmx@latest --lock", cwd=project_name)
    elif choice == "2": # choice == "2"
        run_command("poetry add datastar-py@latest --lock", cwd=project_name)

    if linter_formatter_choice == "1":
        run_command("poetry add --group dev black@latest isort@latest --lock", cwd=project_name)

    if server_choice == "1":
        run_command("poetry add gunicorn@latest --lock", cwd=project_name)
    elif server_choice == "2":
        run_command("poetry add uvicorn[standard]@latest --lock", cwd=project_name)
    elif server_choice == "3":
        run_command("poetry add daphne@latest --lock", cwd=project_name)

    if pre_commit_choice == "1":
        run_command("poetry add --group dev pre-commit@latest --lock", cwd=project_name)