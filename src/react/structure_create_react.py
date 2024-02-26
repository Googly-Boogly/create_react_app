import json
import os
from typing import Dict, Union

from code_creation.architect.react.crud_js_file import create_base_js_file
from prompts.react_frontend import ReactPrompts


def create_react_ai_structure(project_path: str, project_name: str, description_to_build: str,
                              host_os_project_path: str) -> Dict[str, Union[str, Dict[str, str]]]:
    """
    The AI creates the structure for the react project.
    :param project_path: The path to the project.
    :param project_name: The name of the project.
    :param description_to_build: The description of the project to build.
    :param host_os_project_path: The path to the project on the host OS. WILL BE THE HIGH LEVEL WITH ALL OTHER PROJECTS
    :return: The structure of the project.
    """
    scope_blueprint: str = ReactPrompts.create_scope(project_name=project_name,
                              project_description=description_to_build)
    design_blueprint: str = ReactPrompts.designer(project_name=project_name, project_description=description_to_build,
                                                  design_blueprint=scope_blueprint)
    high_level_of_structure: Dict[str, str] = (ReactPrompts
                               .create_high_level_structure(project_reqs=scope_blueprint,
                                                           design_blueprint=design_blueprint))
    # high level structure will represent the 8 main folders of the react project, they can be nothing
    new_structure: Dict[str, Dict[str, str]] = {}
    for folder, folder_blueprint in high_level_of_structure.items():
        if folder_blueprint == "":
            new_structure[folder] = {"empty": "empty"}
            continue
        created_dir: Dict[str, str] = ReactPrompts.create_directory(directory_name=folder,
                                             directory_blueprint=folder_blueprint)
        created_dir["DIRECTORY_README.md"] = folder_blueprint
        new_structure[folder] = created_dir

    # create a structure.md file in the project folder
    with open(f"{project_path}/STRUCTURE_JSON.md", "w") as structure_file:
        structure_file.write(json.dumps(new_structure))
    # Create the scope.md file in the project folder
    with open(f"{project_path}/SCOPE.md", "w") as scope_file:
        scope_file.write(scope_blueprint)
    # Create the design.md file in the project folder
    with open(f"{project_path}/DESIGN.md", "w") as design_file:
        design_file.write(design_blueprint)

    return new_structure


def create_react_physical_structure(project_path: str, structure: Dict[str, Dict[str, str]]):
    """
    Create the physical structure of the react project.
    :param project_path: The path to the project.
    :param structure: The structure of the project.
    :return:
    """
    src_path = os.path.join(project_path, "src")
    for folder, folder_structure in structure.items():
        if folder_structure.get("empty"):
            continue
        folder_path = f"{src_path}/{folder}"
        for file, file_structure in folder_structure.items():
            if file == "empty":
                continue
            create_base_js_file(file_path=f"{folder_path}/{file}", description=file_structure)
    return



