import os
import subprocess

from global_code.helpful_functions import log_it, create_logger_error
from react.setup_react_project import setup_project_react
from react.structure_create_react import create_react_ai_structure, \
    create_react_physical_structure
from react.run_website import run_react_website


def main_workflow_to_create_react_app(projects_folder: str, project_name: str, description_to_build: str,
                                      host_os_project_path: str):
    """
    This function will run the main workflow to create a React project.
    :param projects_folder: The folder to create the project in.
    :param project_name: The name of the project to create.
    :param description_to_build: The description of the project to build.
    :param host_os_project_path: The path to the project on the host OS. WILL BE THE HIGH LEVEL WITH ALL OTHER PROJECTS
    :return:
    """
    # Create the project folder
    project_path = os.path.join(projects_folder, project_name)
    os.makedirs(project_path, exist_ok=True)
    run_react_website
    create_setup_project_sh(project_path)
    create_setup_docker(project_path)
    run_setup_docker_for_react(project_path, project_name, host_os_project_path)
    setup_project_react(projects_folder, project_name, host_os_project_path)

    proj_proj_path = os.path.join(project_path, project_name)
    structure = create_react_ai_structure(proj_proj_path, project_name, description_to_build, host_os_project_path)
    create_react_physical_structure(proj_proj_path, structure=structure)


def create_setup_project_sh(project_path: str):
    """
    Create a setup_project.sh file.
    :param project_path: The path to the project.
    :return:
    """
    content = '''
#!/bin/bash

# Create the project based on the project type
if [ "$PROJECT_TYPE" = "cra" ]; then
    npx create-react-app $PROJECT_NAME
elif [ "$PROJECT_TYPE" = "next" ]; then
    npx create-next-app $PROJECT_NAME
elif [ "$PROJECT_TYPE" = "gatsby" ]; then
    npx gatsby new $PROJECT_NAME
else
    echo "Invalid project type. Please choose 'cra', 'next', or 'gatsby'."
    exit 1
fi


# Navigate to the project directory
cd $PROJECT_NAME

# Add the UI library
if [ "$UI_LIB" == "material-ui" ]; then
    npm install @mui/material @mui/icons-material @emotion/react @emotion/styled
elif [ "$UI_LIB" == "ant-design" ]; then
    npm install antd
elif [ "$UI_LIB" == "chakra-ui" ]; then
    npm install @chakra-ui/react @emotion/react @emotion/styled framer-motion
else
    echo "Invalid UI library. Please choose 'material-ui', 'ant-design', or 'chakra-ui'."
    exit 1
fi

# Add the state management library
if [ "$STATE_MANAGEMENT_LIB" == "redux" ]; then
    npm install redux react-redux
elif [ "$STATE_MANAGEMENT_LIB" == "mobx" ]; then
    npm install mobx mobx-react
fi

# Add testing tools
npm install --save-dev jest @testing-library/react

# Add development tools
npm install --save-dev eslint prettier @storybook/react husky dotenv

chmod -R 755 $PROJECT_NAME

echo "Project $PROJECT_NAME created successfully."

'''
    setup = os.path.join(project_path, 'setup_project.sh')
    with open(setup, 'w') as setup_project_sh:
        setup_project_sh.write(content)


def create_setup_docker(project_path: str):
    """
    Create a setup_docker.sh file.
    :return:
    """
    content = '''
# Use an official Node.js runtime as a parent image
FROM node:latest

# Set the working directory in the container
WORKDIR /app

# Copy a script into the container to set up the project
COPY setup_project.sh /app/

# Make the script executable
RUN chmod +x /app/setup_project.sh

# Run the script to set up the project based on environment variables
CMD ["/bin/bash", "/app/setup_project.sh"]
'''
    setup = os.path.join(project_path, 'Dockerfile.setup')
    with open(setup, 'w') as setup_docker_sh:
        setup_docker_sh.write(content)


def run_setup_docker_for_react(project_path: str, project_name: str, host_os_project_path: str):
    """
    Run the Dockerfile.setup file to set up the project.
    :param project_path: The path to the project.
    :param project_name: The name of the project.
    :param host_os_project_path: The path to the project on the host OS. WILL BE THE HIGH LEVEL WITH ALL OTHER PROJECTS
    :return:
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
    build_command = ["docker", "build", "-f", "Dockerfile.setup", "-t", f"{project_name}_setup", "."]
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
    host_os_proj_path = os.path.join(host_os_project_path, project_name)
    # docker run -v "$(pwd)":/app -e PROJECT_TYPE=cra -e PROJECT_NAME=my-react-app -e UI_LIB=material-ui -e STATE_MANAGEMENT_LIB=redux react-project-setup
    run_command = ["docker", "run", "-u", "1000:1000", "-v", f'{host_os_proj_path}:/app', "-e", "PROJECT_TYPE=cra", "-e", f"PROJECT_NAME={project_name}",
                   "-e", "UI_LIB=material-ui", "-e", "STATE_MANAGEMENT_LIB=redux", f"{project_name}_setup"]
    try:
        log_it(logger, error=None, custom_message="Running the React Setup",
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
