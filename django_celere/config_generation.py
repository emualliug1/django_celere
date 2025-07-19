import os
import logging
from jinja2 import Environment, FileSystemLoader

logger = logging.getLogger(__name__)

# Setup Jinja2 environment
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

def generate_config_files(project_name, js_lib_choice, component_lib_choice, db_choice, linter_formatter_choice, typescript_choice, ci_cd_choice, server_choice, pre_commit_choice):
    """Generates all the necessary configuration files."""

    # Create frontend src directories
    os.makedirs(os.path.join(project_name, "frontend/static/src/js"), exist_ok=True)
    os.makedirs(os.path.join(project_name, "frontend/static/src/css"), exist_ok=True)

    # --- File Content ---

    server_command = ""
    if server_choice == "1":
        server_command = "gunicorn config.wsgi:application --bind 0.0.0.0:8000"
    elif server_choice == "2":
        server_command = "uvicorn config.asgi:application --host 0.0.0.0 --port 8000"
    elif server_choice == "3":
        server_command = "daphne config.asgi:application --bind 0.0.0.0 --port 8000"

    dockerfile_content = env.get_template("Dockerfile.template").render(
        server_command=server_command
    )
    db_service = ""
    db_volume = ""
    if db_choice == "2": # PostgreSQL (Local Docker)
        db_service = env.get_template("docker-compose_postgres_service.template").render()
        db_volume = env.get_template("docker-compose_postgres_volume.template").render()
    elif db_choice == "3": # MySQL (Local Docker)
        db_service = env.get_template("docker-compose_mysql_service.template").render()
        db_volume = env.get_template("docker-compose_mysql_volume.template").render()

    docker_compose_content = env.get_template("docker-compose.template").render(
        db_service=db_service,
        db_volume=db_volume
    )
    nginx_conf_content = env.get_template("nginx.conf.template").render()

    js_lib_app = ""
    js_lib_middleware = ""
    if js_lib_choice == "1":
        js_lib_app = "'django_htmx'"
        js_lib_middleware = "'django_htmx.middleware.HtmxMiddleware'"
    elif js_lib_choice == "2":
        js_lib_app = "'datastar'"
        js_lib_middleware = "'datastar.middleware.DatastarMiddleware'" # Assuming Datastar has a middleware

    db_settings = ""
    if db_choice == "1": # SQLite
        db_settings = "'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'data/db.sqlite3'"
    elif db_choice == "2" or db_choice == "4": # PostgreSQL (Local Docker or Cloud/External)
        db_settings = "'ENGINE': 'django.db.backends.postgresql_psycopg2', 'NAME': os.environ.get('POSTGRES_DB'), 'USER': os.environ.get('POSTGRES_USER'), 'PASSWORD': os.environ.get('POSTGRES_PASSWORD'), 'HOST': os.environ.get('POSTGRES_HOST'), 'PORT': os.environ.get('POSTGRES_PORT', '5432')"
    elif db_choice == "3" or db_choice == "5": # MySQL (Local Docker or Cloud/External)
        db_settings = "'ENGINE': 'django.db.backends.mysql', 'NAME': os.environ.get('MYSQL_DB'), 'USER': os.environ.get('MYSQL_USER'), 'PASSWORD': os.environ.get('MYSQL_PASSWORD'), 'HOST': os.environ.get('MYSQL_HOST'), 'PORT': os.environ.get('MYSQL_PORT', '3306')"

    base_settings_py = env.get_template("base_settings.py.template").render(
        js_lib_app=js_lib_app,
        js_lib_middleware=js_lib_middleware,
        db_settings=db_settings
    )
    dev_settings_py = env.get_template("development_settings.py.template").render()
    prod_settings_py = env.get_template("production_settings.py.template").render()
    settings_init_py = env.get_template("settings_init.py.template").render()

    vite_config_js = env.get_template("vite.config.js.template").render()

    component_lib_import = ""
    if component_lib_choice == "1":
        component_lib_import = "@plugin \"daisyui\";"
    elif component_lib_choice == "2":
        component_lib_import = "@plugin \"flowbite\";"
    app_css_content = env.get_template("app.css.template").render(
        component_lib_import=component_lib_import
    )

    if js_lib_choice == "1":
        js_lib_import = "import 'htmx.org';\nimport 'alpinejs';"
    elif js_lib_choice == "2":
        js_lib_import = "import 'datastar-js';"

    if typescript_choice == "2":
        app_js_content = env.get_template("app.ts.template").render(
            js_lib_import=js_lib_import
        )
    else:
        app_js_content = env.get_template("app.js.template").render(
            js_lib_import=js_lib_import
        )

    js_lib_display = {
        "1": "HTMX + Alpine.js",
        "2": "Datastar.js",
        "3": "None"
    }.get(js_lib_choice, "None")

    component_lib_display = {
        "1": "DaisyUI",
        "2": "Flowbite",
        "3": "None"
    }.get(component_lib_choice, "None")

    base_html = env.get_template("base.html.template").render(
        js_lib_display=js_lib_display,
        component_lib_display=component_lib_display
    )

    manage_py = env.get_template("manage.py.template").render()
    urls_py = env.get_template("urls.py.template").render()

    prettier_script = ""
    if linter_formatter_choice == "1":
        prettier_script = ",\n    \"format\": \"prettier --write .\""





    # --- File Creation ---
    
    files_to_create = {
        os.path.join(project_name, ".env"): env.get_template("env.template").render(),
        os.path.join(project_name, "Dockerfile"): dockerfile_content,
        os.path.join(project_name, "docker-compose.yml"): docker_compose_content,
        os.path.join(project_name, "nginx/nginx.conf"): nginx_conf_content,
        os.path.join(project_name, "backend/manage.py"): manage_py,
        os.path.join(project_name, "backend/config/settings/base.py"): base_settings_py,
        os.path.join(project_name, "backend/config/settings/development.py"): dev_settings_py,
        os.path.join(project_name, "backend/config/settings/production.py"): prod_settings_py,
        os.path.join(project_name, "backend/config/settings/__init__.py"): settings_init_py,
        os.path.join(project_name, "backend/config/urls.py"): urls_py,
        os.path.join(project_name, "frontend/vite.config.js"): vite_config_js,
        
        os.path.join(project_name, "frontend/static/src/css/app.css"): app_css_content,
        os.path.join(project_name, f"frontend/static/src/js/app.{'ts' if typescript_choice == '2' else 'js'}"): app_js_content,
        
        os.path.join(project_name, "Makefile"): env.get_template("Makefile.template").render(),
    }

    if linter_formatter_choice == "1":
        prettierrc_content = env.get_template("prettierrc.template").render()
        files_to_create[os.path.join(project_name, "frontend/.prettierrc")] = prettierrc_content

    if pre_commit_choice == "1":
        pre_commit_config_content = env.get_template("pre-commit-config.yaml.template").render()
        files_to_create[os.path.join(project_name, ".pre-commit-config.yaml")] = pre_commit_config_content

    if server_choice == "2": # Uvicorn (ASGI)
        asgi_py_content = env.get_template("asgi.py.template").render()
        files_to_create[os.path.join(project_name, "backend/config/asgi.py")] = asgi_py_content

    if ci_cd_choice == "1":
        github_actions_content = env.get_template("github_actions.template").render()
        files_to_create[os.path.join(project_name, ".github/workflows/django.yml")] = github_actions_content
    elif ci_cd_choice == "2":
        gitlab_ci_content = env.get_template("gitlab_ci.template").render()
        files_to_create[os.path.join(project_name, ".gitlab-ci.yml")] = gitlab_ci_content

    docs_readme_content = env.get_template("docs_readme.template").render()
    files_to_create[os.path.join(project_name, "README.md")] = docs_readme_content

    # Generate component templates
    

    # Generate Cotton layout templates
    app_html_content = env.get_template("layouts/app.html.template").render()
    files_to_create[os.path.join(project_name, "frontend/templates/cotton/layouts/app.html")] = app_html_content

    base_html_content = env.get_template("layouts/base.html.template").render()
    files_to_create[os.path.join(project_name, "frontend/templates/cotton/layouts/base.html")] = base_html_content

    guest_html_content = env.get_template("layouts/guest.html.template").render()
    files_to_create[os.path.join(project_name, "frontend/templates/cotton/layouts/guest.html")] = guest_html_content

    main_html_content = env.get_template("layouts/main.html.template").render()
    files_to_create[os.path.join(project_name, "frontend/templates/cotton/layouts/main.html")] = main_html_content

    for file_path, content in files_to_create.items():
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            f.write(content)
        logger.debug(f"- Created: {file_path}")