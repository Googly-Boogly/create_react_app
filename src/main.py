import json
import os

from react.create_react_project import main_workflow_to_create_react_app


def main():
    react_proj_name = "wheelchair_celebration"
    proj_path = '/container/projects'
    proj_name = 'password_creator'
    host_os_proj_path = '/home/alex/Documents/Code/ai_projects'
    project_path = os.path.join(proj_path, proj_name)
    src_directory = os.path.join(project_path, 'src')

    react_app_desc = """
    Create a frontend for a school project. We created an electric wheelchair 
    that is controlled by a raspberry pi. This wheelchair has advanced computer vision.
    This wheelchair also has a homebuilt JARVIS.
    The frontend should be a celebration of our work.
    This should be a very static website.
    It does not need to display any realtime data.
    It does not need any api connections.
    This website should have some basic animations.
    There should be no event page
    """
    main_workflow_to_create_react_app(projects_folder=proj_path, project_name=react_proj_name,
                                      description_to_build=react_app_desc, host_os_project_path=host_os_proj_path)


if __name__ == "__main__":
    main()
