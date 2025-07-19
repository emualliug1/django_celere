import subprocess
import typer
import logging

logger = logging.getLogger(__name__)

def run_command(command, cwd="."):
    """Runs a shell command and exits if it fails."""
    logger.debug(f"Running: '{command}' in '{cwd}'...")
    try:
        result = subprocess.run(command, shell=True, check=True, cwd=cwd, capture_output=True, text=True)
        if result.stdout:
            logger.debug(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed with exit code {e.returncode}")
        if e.stdout:
            logger.error(f"STDOUT:\n{e.stdout}")
        if e.stderr:
            logger.error(f"STDERR:\n{e.stderr}")
        raise
    except FileNotFoundError:
        command_name = command.split()[0]
        logger.error(f"Command not found: '{command_name}'. Is it installed and in your PATH?")
        raise