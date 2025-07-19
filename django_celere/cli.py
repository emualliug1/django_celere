import typer
import os
import shutil
import logging
import time
import sys
from rich.progress import Progress, SpinnerColumn, TextColumn

from django_celere.prompts import (
    get_frontend_choice,
    get_component_library_choice,
    get_database_choice,
    get_linter_formatter_choice,
    get_typescript_choice,
    get_ci_cd_choice,
    get_server_choice,
    get_pre_commit_choice
)
from django_celere.backend_setup import setup_backend
from django_celere.frontend_setup import setup_frontend
from django_celere.config_generation import generate_config_files
from django_celere.django_app_creation import create_django_apps
from django_celere.project_setup import create_directories
from django_celere.utils import logger

app = typer.Typer()

# --- Colors Class ---
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    ORANGE = '\033[38;2;255;165;0m'
    PURPLE = '\033[38;2;147;112;219m'
    PINK = '\033[38;2;255;20;147m'
    LIME = '\033[38;2;50;205;50m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'
    BLINK = '\033[5m'

# --- Helper Functions ---
def clear_screen():
    """Efface l'écran du terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def animate_logo():
    """Anime l'affichage du logo"""
    logo = """
 ██████╗███████╗██╗     ███████╗██████╗ ███████╗
██╔════╝██╔════╝██║     ██╔════╝██╔══██╗██╔════╝
██║     █████╗  ██║     █████╗  ██████╔╝█████╗  
██║     ██╔══╝  ██║     ██╔══╝  ██╔══██╗██╔╝  
╚██████╗███████╗███████╗███████╗██║  ██║███████╗
 ╚═════╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝
"""
    gradient_colors = [
        Colors.RED + Colors.BOLD,
        Colors.ORANGE + Colors.BOLD,
        Colors.YELLOW + Colors.BOLD,
        Colors.LIME + Colors.BOLD,
        Colors.CYAN + Colors.BOLD,
        Colors.BLUE + Colors.BOLD,
        Colors.PURPLE + Colors.BOLD,
    ]
    lines = logo.strip().split('\n')
    for i, line in enumerate(lines):
        color = gradient_colors[i % len(gradient_colors)]
        print(color + line + Colors.RESET)
        time.sleep(0.05)

def print_subtitle():
    """Imprime le sous-titre avec effets"""
    subtitle = "⚡ VITESSE • ÉLÉGANCE • PERFORMANCE ⚡"
    print("\n" + " " * 15 + Colors.CYAN + Colors.BOLD + subtitle + Colors.RESET)
    print(" " * 25 + Colors.DIM + "--- Terminal Ready ---" + Colors.RESET)
    print("\n")

@app.command()
def main(project_name: str = typer.Argument(..., help="The name of the Django project to create.")):
    """Celere: An ultra-fast tool to initialize and structure your Django projects."""
    clear_screen()
    animate_logo()
    print_subtitle()

    # Configure logging for the CLI
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    # Set a higher level for the project's logger during progress to suppress INFO messages
    project_logger = logging.getLogger("django_celere")
    original_level = project_logger.level
    project_logger.setLevel(logging.WARNING)

    try:
        # 1. Get user choices
        js_lib_choice = get_frontend_choice()
        component_lib_choice = get_component_library_choice()
        db_choice = get_database_choice()
        linter_formatter_choice = get_linter_formatter_choice()
        typescript_choice = get_typescript_choice()
        ci_cd_choice = get_ci_cd_choice()
        server_choice = get_server_choice()
        pre_commit_choice = get_pre_commit_choice()

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            # 2. Create directory structure
            task_dirs = progress.add_task("[cyan]Creating project directories...", total=1)
            create_directories(project_name)
            progress.update(task_dirs, completed=1)

            # 3. Setup Backend
            task_backend = progress.add_task("[cyan]Setting up Backend...", total=1)
            setup_backend(project_name, js_lib_choice, linter_formatter_choice, server_choice, pre_commit_choice)
            progress.update(task_backend, completed=1)

            # 4. Setup Frontend
            task_frontend = progress.add_task("[cyan]Setting up Frontend...", total=1)
            setup_frontend(project_name, js_lib_choice, component_lib_choice, linter_formatter_choice, typescript_choice)
            progress.update(task_frontend, completed=1)

            # 5. Generate Configuration Files
            task_config = progress.add_task("[cyan]Generating Configuration Files...", total=1)
            generate_config_files(project_name, js_lib_choice, component_lib_choice, db_choice, linter_formatter_choice, typescript_choice, ci_cd_choice, server_choice, pre_commit_choice)
            progress.update(task_config, completed=1)

            # 6. Create Django Apps
            task_apps = progress.add_task("[cyan]Creating Django Apps...", total=1)
            create_django_apps(project_name)
            progress.update(task_apps, completed=1)

        # Restore original logger level after progress bar
        project_logger.setLevel(original_level)

        logger.info("🚀 Project setup complete! 🚀")
        logger.info("\nNext Steps:")
        logger.info(f"1. cd {project_name}/")
        logger.info("2. poetry run python manage.py runserver")
        logger.info("3. In another terminal, cd frontend/ && npm run dev")
        logger.info("4. Open http://127.0.0.1:8000 in your browser.")

    except (typer.Exit, KeyboardInterrupt):
        project_logger.setLevel(original_level) # Restore level on error
        logger.error(f"Project setup cancelled.")
        if project_name and os.path.exists(project_name):
            logger.info(f"Attempting to clean up partially created project directory: {project_name}")
            try:
                shutil.rmtree(project_name)
                logger.info(f"Successfully removed {project_name}")
            except OSError as cleanup_error:
                logger.error(f"Error during cleanup of {project_name}: {cleanup_error}")
        typer.echo(f"\n[ABORTED] Project setup cancelled by user.", err=True)
        raise typer.Exit(code=1)
    except Exception as e:
        project_logger.setLevel(original_level) # Restore level on error
        logger.exception(f"An unexpected error occurred during project setup: {e}")
        if project_name and os.path.exists(project_name):
            logger.info(f"Attempting to clean up partially created project directory: {project_name}")
            try:
                shutil.rmtree(project_name)
                logger.info(f"Successfully removed {project_name}")
            except OSError as cleanup_error:
                logger.error(f"Error during cleanup of {project_name}: {cleanup_error}")
        typer.echo(f"\n[ERROR] Project setup failed. Please check the logs for details.", err=True)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()