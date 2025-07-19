<p>
  <img src="https://github.com/emualliug1/django_celere/raw/main/logo.png" alt="Celere Logo" width="200">
</p>

# Celere ⚡

## Celere: An Ultra-Fast Django Project Initializer

**Celere** is an ultra-fast command-line interface (CLI) tool designed to initialize and structure modern Django projects with a focus on best practices and developer efficiency. It automates the setup of a full-stack web application, integrating Django for the backend with a modern JavaScript frontend build system (Vite) and styling (Tailwind CSS).

## Why Celere?

-   **Instant Start**: Get a production-ready Django project up and running in seconds.
-   **Automated Configuration**: Automatically sets up modern development standards, including Docker, Vite, Tailwind CSS, and Poetry for dependency management.
-   **Isolated Environments**: Ensures that the generated project's dependencies are completely isolated from Celere's own dependencies, preventing conflicts.
-   **Flexible Frontend Choices**: Offers interactive prompts to select your preferred JavaScript library (HTMX & Alpine.js, DataStar.js, or Vanilla JS) and component library (DaisyUI, Flowbite, or None).
-   **Modern Tooling**: Integrates with Prettier for code formatting and supports TypeScript for robust frontend development.
-   **Intuitive CLI**: A simple command is all you need: `celere myproject`.
-   **Best Practices Included**: Comes with split Django settings, a pre-configured `.gitignore`, and a logical application structure.

## Installation

To install Celere globally on your system, follow these steps:

1.  **Install pipx**: If you don't have `pipx` installed, you can install it using `pip`:
    ```bash
    pip install pipx
    pipx ensurepath
    ```
    *You might need to restart your terminal after running `pipx ensurepath`.*

    **1.1. Ensure pipx executables are in your PATH**:
    After `pipx ensurepath`, the directory where `pipx` installs executables (usually `~/.local/bin` or `~/Library/Python/X.Y/bin` on macOS) needs to be in your system's `PATH` environment variable. If `celere` command is not found, follow these steps:

    *   **Check your PATH**:
        ```bash
        echo $PATH
        ```
    *   **Find pipx's bin directory**:
        ```bash
        pipx completions
        # Look for a line like: "Add the following to your shell config file: ... ~/.local/bin ..."
        # Or, on macOS, it might be something like /Users/your_username/Library/Python/3.X/bin
        ```
    *   **Add to your shell configuration file** (e.g., `~/.zshrc`, `~/.bashrc`, `~/.profile`):
        Open the file with a text editor (e.g., `nano ~/.zshrc`) and add the following line at the end, replacing `YOUR_PIPX_BIN_PATH` with the actual path found above:
        ```bash
        export PATH="YOUR_PIPX_BIN_PATH:$PATH"
        ```
        Example for macOS Python 3.13:
        ```bash
        export PATH="/Users/your_username/Library/Python/3.13/bin:$PATH"
        ```
    *   **Apply changes**: Close and reopen your terminal, or run `source ~/.zshrc` (or your respective shell config file).

2.  **Install Celere using pipx**:
    ```bash
    pipx install django-celere # This assumes 'django-celere' is published on PyPI
    ```
    *If you are developing Celere itself, you can install it in editable mode from its source directory: `pipx install --editable .` from the project root.*

## Usage

1.  **Navigate to the directory where you want to create your new project**:
    ```bash
    cd /path/to/your/projects
    ```

2.  **Run the initialization command**:
    ```bash
    celere myproject_name
    ```
    Replace `myproject_name` with your desired project name.

3.  **Follow the interactive prompts**: Celere will guide you through choices for your frontend stack, database, linters, and more.

    Example prompts:
    -   `Enter the project name:`
    -   `Choose JavaScript Library/Framework:` (HTMX & Alpine.js, DataStar.js, None)
    -   `Choose Tailwind Component Library:` (DaisyUI, Flowbite, None)
    -   `Choose JavaScript or TypeScript:` (JavaScript, TypeScript)
    -   `Choose Linter/Formatter Options:` (Black & isort + Prettier, None)
    -   `Choose Database:` (SQLite, PostgreSQL, MySQL)
    -   `Choose CI/CD Pipeline:` (GitHub Actions, GitLab CI/CD, None)
    -   `Choose Server:` (Gunicorn, Uvicorn, Daphne)
    -   `Choose Pre-Commit Hooks:` (Yes, No)

4.  **Once the script is finished, your project is ready!**

## Generated Project Structure

Celere generates a well-structured Django project with a clear separation of backend and frontend concerns. Key directories include:

-   **`myproject/` (Root)**: Contains `docker-compose.yml`, `Dockerfile`, `Makefile`, `pyproject.toml`, `poetry.lock`, and the main `README.md`.
-   **`myproject/backend/`**: Your Django application, including `manage.py`, `apps/` (for modular Django apps), and `config/` (for Django settings, URLs, WSGI/ASGI).
-   **`myproject/frontend/`**: Your Vite-powered frontend application, including `package.json`, `vite.config.js`, `static/` (for static assets), and `templates/` (for Django templates).
-   **`myproject/data/`**: Intended for persistent data (e.g., SQLite database).
-   **`myproject/media/`**: Directory for user-uploaded files.
-   **`myproject/nginx/`**: Contains Nginx configuration for serving the application.

## Key Technologies (Generated Projects)

-   **Backend**: Django (Python)
-   **Frontend Build**: Vite (JavaScript/TypeScript)
-   **Styling**: Tailwind CSS
-   **Python Dependency Management**: Poetry
-   **JavaScript Dependency Management**: npm
-   **Containerization**: Docker
-   **Web Server**: Nginx


## License

This project is licensed under the MIT License - see the `LICENSE` file for details.