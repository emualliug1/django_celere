import os
import logging
from jinja2 import Environment, FileSystemLoader
from .utils import run_command

logger = logging.getLogger(__name__)

def generate_frontend_readme(project_name, js_lib_choice, component_lib_choice):
    """Generates a README.md for the frontend using a Jinja2 template."""
    template_dir = os.path.join(os.path.dirname(__file__), "templates")
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("frontend_readme.template")

    js_lib_map = {
        "1": "HTMX & Alpine.js",
        "2": "DataStar.js",
        "3": "None (Vanilla JS)"
    }
    component_lib_map = {
        "1": "DaisyUI",
        "2": "Flowbite",
        "3": "None"
    }

    context = {
        "js_lib": js_lib_map.get(js_lib_choice, "Unknown"),
        "component_lib": component_lib_map.get(component_lib_choice, "Unknown")
    }

    readme_content = template.render(context)

    readme_path = os.path.join(project_name, "frontend", "README.md")
    os.makedirs(os.path.dirname(readme_path), exist_ok=True)
    with open(readme_path, "w") as f:
        f.write(readme_content)
    logger.debug(f"  Generated README.md for frontend at {readme_path}")

def _get_frontend_dependencies(js_lib_choice, component_lib_choice, typescript_choice, linter_formatter_choice):
    dependencies = []
    dev_dependencies = []

    # Base dependencies for Vite
    dev_dependencies.append("\"vite\": \"latest\"")

    # JavaScript Library/Framework dependencies
    if js_lib_choice == "1":  # HTMX & Alpine.js
        # HTMX and Alpine.js are typically included via CDN or directly in HTML, not npm packages for a simple setup
        pass
    elif js_lib_choice == "2":  # DataStar.js
        dependencies.append("\"DataStar\": \"^0.1.0\"") # Placeholder version
    elif js_lib_choice == "3":  # None (Vanilla JS)
        pass

    # Component Library dependencies
    if component_lib_choice == "1":  # DaisyUI
        dev_dependencies.append("\"daisyui\": \"latest\"") # Placeholder version
    elif component_lib_choice == "2":  # Flowbite
        dev_dependencies.append("\"flowbite\": \"latest\"") # Placeholder version

    # TypeScript dependencies
    if typescript_choice == "2": # TypeScript
        dev_dependencies.append("\"typescript\": \"latest\"")
        dev_dependencies.append("\"@types/node\": \"latest\"") # Placeholder version

    # Linter/Formatter dependencies
    if linter_formatter_choice == "1": # Prettier
        dev_dependencies.append("\"prettier\": \"latest\"")

    # Tailwind CSS dependencies (always included as per project structure)
    dev_dependencies.append("\"tailwindcss\": \"latest\"")
    dev_dependencies.append("\"@tailwindcss/vite\": \"latest\"")
    

    return ",\n    ".join(dependencies), ",\n    ".join(dev_dependencies)

def setup_frontend(project_name, js_lib_choice, component_lib_choice, linter_formatter_choice, typescript_choice):
    """Initializes frontend project and installs dependencies using NPM."""
    
    frontend_dir = os.path.join(project_name, "frontend")
    
    # Generate package.json with dynamic dependencies
    template_dir = os.path.join(os.path.dirname(__file__), "templates")
    env = Environment(loader=FileSystemLoader(template_dir))
    package_json_template = env.get_template("package.json.template")

    dependencies_str, dev_dependencies_str = _get_frontend_dependencies(js_lib_choice, component_lib_choice, typescript_choice, linter_formatter_choice)

    package_json_content = package_json_template.render(
        dependencies=dependencies_str,
        dev_dependencies=dev_dependencies_str,
        project_name=project_name, # Pass project_name for template rendering
        prettier_script="" # Placeholder for prettier script, if needed
    )

    package_json_path = os.path.join(frontend_dir, "package.json")
    os.makedirs(os.path.dirname(package_json_path), exist_ok=True)
    with open(package_json_path, "w") as f:
        f.write(package_json_content)
    logger.debug(f"  Generated package.json at {package_json_path}")

    run_command("npm install", cwd=frontend_dir)

    # Generate frontend README.md
    generate_frontend_readme(project_name, js_lib_choice, component_lib_choice)