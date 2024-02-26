import os
import subprocess
from typing import Optional


def setup_project_react(project_path_input: str, project_name: str,
                  host_os_project_path: str) -> None:
    """
    Sets up a react project in a safe, containerized environment.
    Creates Dockerfile, docker-compose.yaml
    And .gitignore file, and .dockerignore file.
    Create the basic layout of the react project as well.
    Parameters:
    - project_path_input (str): The path to the projects folder. IE THE ONE WITH OTHER PROJECTS
    - project_name (str): The name of the project.
    - host_os_project_path (str): The path to the project on the host OS. HIGH LEVEL WITH OTHER PROJECTS
    Returns:
        NA
    """
    # Step 1: Generate requirements.txt and README.md within the project folder

    project_path = os.path.join(project_path_input, project_name)
    project_path2 = os.path.join(project_path, project_name)
    host_os = os.path.join(host_os_project_path, project_name)
    host_os2 = os.path.join(host_os, project_name)
    docker_compose_content = create_docker_compose_file(host_os2, project_name)
    dockerfile_content = create_dockerfile()
    gitignore_content = create_gitignore_file()
    dockerignore_content = create_dockerignore_file()
    src_directory = os.path.join(project_path2, 'src')
    components_directory = os.path.join(src_directory, 'components')
    hooks_directory = os.path.join(src_directory, 'hooks')
    pages_directory = os.path.join(src_directory, 'pages')
    utils_directory = os.path.join(src_directory, 'utils')
    assets_directory = os.path.join(src_directory, 'assets')
    context_directory = os.path.join(src_directory, 'context')
    services_directory = os.path.join(src_directory, 'services')
    routes_directory = os.path.join(src_directory, 'routes')
    dockerignore_file_path = os.path.join(project_path2, '.dockerignore')
    gitignore_file_path = os.path.join(project_path2, '.gitignore')

    os.makedirs(components_directory, exist_ok=True)
    os.makedirs(hooks_directory, exist_ok=True)
    os.makedirs(pages_directory, exist_ok=True)
    os.makedirs(utils_directory, exist_ok=True)
    os.makedirs(assets_directory, exist_ok=True)
    os.makedirs(context_directory, exist_ok=True)
    os.makedirs(services_directory, exist_ok=True)
    os.makedirs(routes_directory, exist_ok=True)

    with open(dockerignore_file_path, 'w') as req_file:
        req_file.write(dockerignore_content)

    with open(gitignore_file_path, 'w') as req_file:
        req_file.write(gitignore_content)

    with open(os.path.join(project_path2, 'Dockerfile.prod'), 'w') as dockerfile:
        dockerfile.write(dockerfile_content)

    with open(os.path.join(project_path2, 'docker-compose.yaml'), 'w') as docker_compose:
        docker_compose.write(docker_compose_content)


def create_gitignore_file() -> str:
    """
    Creates a .gitignore file in the project folder.

    Returns:
    str: The content of the .gitignore file.
    """
    gitignore_content = f"""
########################################################################################
# Telomere

# NORMAL GITIGNORE CONTENT

# Dependency directories
node_modules/

# Production build folder
/build

# dotenv environment variables file
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Debugging logs
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# IDE and editor directories
.idea/
.vscode/
*.swp
*.swo
*.sublime-workspace

# Optional npm cache directory
.npm

# Optional eslint cache
.eslintcache

# Optional REPL history
.node_repl_history

# Output of 'npx create-react-app'
.pnp
.pnp.js

# macOS files
.DS_Store

# Windows files
Thumbs.db

# Optional Yarn v2
.yarn/*
!.yarn/patches/
!.yarn/plugins/
!.yarn/releases/
!.yarn/sdks/
!.yarn/versions/

# END NORMAL GITIGNORE CONTENT

.venv
.env
.secrets
.src/secrets
google_oauth_2_details.json
src/secrets/token.pickle
config.yaml
.src/config.yaml
.models
.db_volume

# Telomere
########################################################################################
"""
    return gitignore_content


def create_dockerignore_file() -> str:
    """
    Creates a .dockerignore file in the project folder.

    Returns:
    str: The content of the .dockerignore file.
    """
    dockerignore_content = f"""
########################################################################################
# Telomere

.venv
.env.sample
src/config.example.yaml
config.example.yaml
.node_modules
node_modules/

# Telomere
########################################################################################
"""
    return dockerignore_content


def create_config_yaml_file(config_yaml: str) -> str:
    """
    Creates a config.yaml file in the project folder.

    Returns:
    str: The content of the config.yaml file.
    """
    config_yaml_content = f"""
########################################################################################
# Telomere

{config_yaml}

# Telomere
########################################################################################
"""
    return config_yaml_content


def create_readme_file(readme: str) -> str:
    """
    Creates a README.md file in the project folder.

    Returns:
    str: The content of the README.md file.
    """
    readme_content = f"""
########################################################################################
# Telomere

{readme}

# Telomere
########################################################################################
"""
    return readme_content


def create_dockerfile() -> str:
    """
    Creates a Dockerfile in the project folder.

    Returns:
    str: The content of the Dockerfile.
    """
    dockerfile_content = f"""
########################################################################################
# Telomere

# Stage 1: Build the React application
FROM node:16 as build

# Set the working directory in the builder stage
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of your app's source code
COPY . .

# Build your app
RUN npm run build

# Stage 2: Serve the app with Nginx
FROM nginx:alpine

# Copy the build output to replace the default nginx contents.
COPY --from=build /app/build /usr/share/nginx/html

# Expose port 80 to the outside once the container has launched
EXPOSE 80

# Tell Docker about the port we'll run on.
CMD ["nginx", "-g", "daemon off;"]

# Telomere
########################################################################################
"""
    return dockerfile_content


def create_docker_compose_file(project_path: str, project_name: str) -> str:
    """
    Creates a docker-compose.yaml file in the project folder.

    Parameters:
    - project_path (str): The path to the project folder.
    - project_name (str): The name of the project.

    Returns:
    str: The content of the docker-compose.yaml file.
    """
    docker_compose_content = f"""
########################################################################################
# Telomere

version: '3.8'

services:
  {project_name}:
    container_name: {project_name}
    build:
      context: .
      dockerfile: Dockerfile.prod
    ports:
      - "80:80"


# Telomere
########################################################################################
"""
    return docker_compose_content


def create_config_yaml_example_file(config_yaml_example: str) -> str:
    """
    Creates a config.example.yaml file in the project folder.

    Returns:
    str: The content of the config.example.yaml file.
    """
    config_yaml_content = f"""
########################################################################################
# Telomere

{config_yaml_example}

# Telomere
########################################################################################
"""
    return config_yaml_content


if __name__ == "__main__":
    setup_project_react("/path/to/your/project", "requirements.txt", "project_name")
    # run_project()

