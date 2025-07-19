import os
import logging

logger = logging.getLogger(__name__)

def create_directories(project_name):
    """Creates the project directory structure."""
    # Define project structure dynamically based on project_name
    PROJECT_STRUCTURE = {
        os.path.join(project_name, "backend"): ["apps", "config/settings"],
        os.path.join(project_name, "frontend"): ["static/src/js", "static/src/css", "templates", os.path.join("templates", "cotton"), os.path.join("templates", "cotton", "forms"), os.path.join("templates", "cotton", "navigation"), os.path.join("templates", "cotton", "overlays"), os.path.join("templates", "cotton", "utils")],
        os.path.join(project_name, "data"): [],
        os.path.join(project_name, "media"): [],
        os.path.join(project_name, "nginx"): [],
        
    }

    for base_dir, sub_dirs in PROJECT_STRUCTURE.items():
        os.makedirs(base_dir, exist_ok=True)
        logger.debug(f"- Created: {base_dir}/")
        for sub_dir in sub_dirs:
            path = os.path.join(base_dir, sub_dir)
            os.makedirs(path, exist_ok=True)
            logger.debug(f"  - Created: {path}/")