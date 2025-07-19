import os
import shutil
from .utils import run_command

def create_django_apps(project_name):
    """Creates the core and authentication Django apps."""
    run_command(f"poetry run django-admin startapp core", cwd=project_name)
    shutil.move(os.path.join(project_name, "core"), os.path.join(project_name, "backend", "apps", "core"))
    run_command(f"poetry run django-admin startapp authentication", cwd=project_name)
    shutil.move(os.path.join(project_name, "authentication"), os.path.join(project_name, "backend", "apps", "authentication"))