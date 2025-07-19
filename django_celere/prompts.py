import questionary

def get_frontend_choice():
    """Prompts the user to choose a JavaScript library/framework."""
    choice = questionary.select(
        "Choose JavaScript Library/Framework",
        choices=[
            "HTMX & Alpine.js",
            "DataStar.js",
            "None (Vanilla JS)",
        ],
    ).ask()
    if choice == "HTMX & Alpine.js":
        return "1"
    elif choice == "DataStar.js":
        return "2"
    else:
        return "3"

def get_component_library_choice():
    """Prompts the user to choose a Tailwind component library."""
    choice = questionary.select(
        "Choose Tailwind Component Library (Optional)",
        choices=[
            "DaisyUI",
            "Flowbite",
            "None",
        ],
    ).ask()
    if choice == "DaisyUI":
        return "1"
    elif choice == "Flowbite":
        return "2"
    else:
        return "3"

def get_database_choice():
    """Prompts the user to choose a database."""
    choice = questionary.select(
        "Choose Database",
        choices=[
            "SQLite (Default)",
            "PostgreSQL (Local Docker)",
            "MySQL (Local Docker)",
            "PostgreSQL (Cloud/External)",
            "MySQL (Cloud/External)",
        ],
    ).ask()
    if choice == "SQLite (Default)":
        return "1"
    elif choice == "PostgreSQL (Local Docker)":
        return "2"
    elif choice == "MySQL (Local Docker)":
        return "3"
    elif choice == "PostgreSQL (Cloud/External)":
        return "4"
    else:
        return "5"

def get_linter_formatter_choice():
    """Prompts the user to choose linter/formatter options."""
    choice = questionary.select(
        "Choose Linter/Formatter Options",
        choices=[
            "Black & isort (Python) + Prettier (JS/CSS)",
            "None",
        ],
    ).ask()
    if choice == "Black & isort (Python) + Prettier (JS/CSS)":
        return "1"
    else:
        return "2"

def get_typescript_choice():
    """Prompts the user to choose whether to use TypeScript."""
    choice = questionary.select(
        "Choose JavaScript or TypeScript",
        choices=[
            "JavaScript",
            "TypeScript",
        ],
    ).ask()
    if choice == "JavaScript":
        return "1"
    else:
        return "2"

def get_app_choices():
    """Prompts the user to choose specific Django applications to generate."""
    choices = questionary.checkbox(
        'Choose Optional Django Applications (press space to select, enter to confirm)',
        choices=[
            "Users App (with custom User model)",
            "Blog App",
            "Pages App",
        ]).ask()
    
    mapping = {
        "Users App (with custom User model)": "1",
        "Blog App": "2",
        "Pages App": "3",
    }
    
    return [mapping[choice] for choice in choices]

def get_ci_cd_choice():
    """Prompts the user to choose a CI/CD pipeline."""
    choice = questionary.select(
        "Choose CI/CD Pipeline (Optional)",
        choices=[
            "GitHub Actions",
            "GitLab CI/CD",
            "None",
        ],
    ).ask()
    if choice == "GitHub Actions":
        return "1"
    elif choice == "GitLab CI/CD":
        return "2"
    else:
        return "3"

def get_server_choice():
    """Prompts the user to choose a server."""
    choice = questionary.select(
        "Choose Server",
        choices=[
            "Gunicorn (WSGI)",
            "Uvicorn (ASGI)",
            "Daphne (ASGI)",
        ],
    ).ask()
    if choice == "Gunicorn (WSGI)":
        return "1"
    elif choice == "Uvicorn (ASGI)":
        return "2"
    else:
        return "3"

def get_pre_commit_choice():
    """Prompts the user to choose whether to use pre-commit hooks."""
    choice = questionary.select(
        "Choose Pre-Commit Hooks (Optional)",
        choices=[
            "Yes",
            "No",
        ],
    ).ask()
    if choice == "Yes":
        return "1"
    else:
        return "2"
