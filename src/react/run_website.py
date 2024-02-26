import os
import subprocess
from typing import Optional

from global_code.helpful_functions import log_it, create_logger_error


def run_react_website(project_path: str, type_of_run: str):
    """
    This function will start up the react website
    :param project_path: The path to the project folder.
    :param type_of_run: The type of environment to run the project in. It Can be either 'docker' or 'docker_compose'.
    :return:
    """
    if type_of_run == 'docker':
        run_with_docker(project_path)
    elif type_of_run == 'docker_compose':
        x = run_with_docker_compose(project_path)
        # clear_docker_logs(project_path)
        return x


def run_with_docker(project_path: str):
    """
    Runs the Python project in a safe, containerized environment using Docker.
    :param project_path: The path to the project folder.
    :return: NA
    """
    logger = create_logger_error(os.path.abspath(__file__), 'run_project', log_to_console=True,
                                 log_to_file=True)

    # Verify Docker is installed and accessible
    try:
        subprocess.run(["docker", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        what_to_log = "Docker is not installed or not found in PATH. Please ensure Docker is properly installed."
        log_it(logger, error=None, custom_message=what_to_log, log_level='critical')
        return
    except Exception as e:
        what_to_log = "An unexpected error occurred while verifying Docker installation"
        log_it(logger, error=e, custom_message=what_to_log, log_level='critical')
        return

    # Step 1: Build the Docker container
    build_command = ["docker", "build", "-t", "python_project_container", "."]
    try:
        log_it(logger, error=None, custom_message="Building Docker container for the Python project...",
               log_level='info')
        subprocess.run(build_command, check=True, cwd=project_path)
    except subprocess.CalledProcessError:
        log_it(logger, error=None, custom_message="Failed to build the Docker container. Please check your Dockerfile.",
               log_level='critical')
        return
    except Exception as e:
        log_it(logger, error=e, custom_message="An unexpected error occurred during the build process",
               log_level='critical')
        return

    # Step 2: Run the Docker container
    run_command = ["docker", "run", "--rm", "python_project_container"]
    try:
        log_it(logger, error=None, custom_message="Running the Python project in a Docker container...",
               log_level='info')
        subprocess.run(run_command, check=True, cwd=project_path)
    except subprocess.CalledProcessError:
        log_it(logger, error=None,
               custom_message="Failed to run the Docker container. Please check if the container's entry "
                              "point is correctly set up.",
               log_level='critical')
        return
    except Exception as e:
        log_it(logger, error=e, custom_message="An unexpected error occurred while running the container",
               log_level='critical')
        return
    log_it(logger, error=None, custom_message="Python project ran successfully in a Docker container.",
           log_level='info')


def run_with_docker_compose(project_path: str) -> Optional[str]:
    """
    Runs the Python project in a safe, containerized environment using Docker Compose.
    :param project_path: The path to the project folder.
    :return: Either None or the output of the process
    """
    logger = create_logger_error(os.path.abspath(__file__), 'run_project', log_to_console=True,
                                 log_to_file=False)

    # Verify Docker is installed and accessible
    try:
        subprocess.run(["docker", "--version"], check=True, stderr=subprocess.PIPE, text=True)
    except subprocess.CalledProcessError:
        what_to_log = "Docker is not installed or not found in PATH. Please ensure Docker is properly installed."
        log_it(logger, error=None, custom_message=what_to_log, log_level='critical')
        return
    except Exception as e:
        what_to_log = "An unexpected error occurred while verifying Docker installation"
        log_it(logger, error=e, custom_message=what_to_log, log_level='critical')
        return

    # Step 1: Run docker compose
    build_command = ["docker-compose", "up", "--build"]
    logs_command = ["docker-compose", "logs"]
    try:
        log_it(logger, error=None, custom_message="Running docker_compose.yml file container for the React project...",
               log_level='info')
        output2 = subprocess.run(build_command, check=True, cwd=project_path, stderr=subprocess.PIPE, text=True)
        output = subprocess.run(logs_command, check=True, cwd=project_path, capture_output=True, text=True)
    except subprocess.CalledProcessError as err:
        log_it(logger, error=None, custom_message=f"Something went wrong with subprocess.CalledProcessError {err}",
               log_level='critical')
        return
    except Exception as e:
        log_it(logger, error=e, custom_message="An unexpected error occurred during the build process",
               log_level='critical')
        return

    log_it(logger, error=None, custom_message="React project ran successfully in a Docker container.",
           log_level='info')

    return output.stdout


def clear_docker_logs(project_path: str):
    """
    Clears Docker logs by removing containers associated with the project.
    Args:
    - project_path (str): The path to the project folder where the docker-compose.yml is located.
    """
    down_command = ["docker-compose", "down"]
    try:
        # Execute docker-compose down to stop and remove containers
        subprocess.run(down_command, check=True, cwd=project_path, stderr=subprocess.PIPE, text=True)
    except subprocess.CalledProcessError as e:
        print("Error stopping and removing containers:", e.stderr)
    except Exception as e:
        print("An unexpected error occurred:", e)