import os
from typing import Dict, Union, Optional, List

from api_calls.call_any_llm import make_multi_provider_call
from prompts.cleaning_outputs import clean_and_convert_llm_response, extract_code_from_output
from prompts.json_reply import try_json_response
from global_code.helpful_functions import create_logger_error, log_it
logger = create_logger_error(os.path.abspath(__file__), "react_prompts",
                             log_to_console=True, log_to_file=True)

class ReactPrompts:
    def __init__(self):
        self._components = []

    @staticmethod
    def create_scope(project_name: str, project_description: str) -> str:
        """
        Creates a project scope document for the project.

        Returns:
        str: The content of the project scope document.
        """
        project_scope_content = f'''
Project Name: {project_name}

Project Description: {project_description}

Instructions for AI:

Using the project name and description provided above, create a detailed project scope document tailored for a React frontend development. The document should include the following sections:

    Introduction:
        Briefly restate the project's objectives and its significance.

    Target Audience:
        Identify the primary users of the website and any specific user needs or preferences.

    Functional Requirements:
        List the key functionalities that the website must support. Detail how these functionalities will benefit the target audience and meet the project objectives.

    Design Considerations:
        Outline any known design preferences or constraints, such as color schemes, branding elements, or layout structures. Mention if responsive design is a requirement.

    User Roles and Permissions:
        Describe the different user roles that will interact with the website, including any specific permissions or access controls required for each role.

    Key Features and Prioritization:
        Detail the core features of the website, organized by priority. Explain why each feature is critical to the project's success and how it aligns with the overall objectives.

    Conclusion:
        Summarize the scope document, emphasizing the project's goals and how the outlined scope will achieve them.
'''
        first_blueprint: str = (make_multi_provider_call(call_type="llm", provider="openai",
                                                  input_text=project_scope_content,
                                                  config={"model": "gpt-3.5-turbo-0125",
                                                          "type_of_response": "text_only"},
                                                  kwargs={"temperature": 0.8}))

        refine_prompt = f'''
Project Name: {project_name}

Project Description: {project_description}

Initial Project Scope Document:
{first_blueprint}

Instructions for AI:

Given the project name, description, and the initial project scope document provided above, proceed with a detailed review and refinement of the scope document focusing on the React frontend development. Your refinements should address the following objectives:

    Accuracy Verification:
        Confirm that all functionalities, technical specifications, and design elements mentioned are accurate and achievable within the React framework. Ensure they align with the project description.

    Relevance and Contribution:
        Critically assess each section for its relevance to the project's goals. Eliminate or modify elements that do not directly contribute to the objectives.

    Enhancement of Details:
        Expand on the details of key functionalities, features, and technical requirements. Provide specific recommendations for implementation or clarification on how they address user needs.

    Consistency and Clarity Improvement:
        Ensure the document is consistent in its use of terms and clear in its descriptions. Rectify any contradictions or ambiguities.

    User Experience (UX) Considerations:
        Reevaluate the user roles and permissions to ensure a seamless UX for all types of users. Suggest improvements where necessary.

    Design Considerations Update:
        Update the design considerations to reflect current web design trends that are compatible with React. Focus on elements that enhance usability and the overall user experience.

    Incorporation of Feedback:
        If there's any feedback or additional information provided on the initial scope, incorporate this into the refinement process.

    Final Adjustments and Recommendations:
        Offer any final suggestions for adjustments or additions that would refine the scope, aiming for the project's success.

    Conclusive Summary:
        Provide a concise summary of the key refinements made to the scope document, emphasizing the improvements and their intended impact on the project.
'''
        refined_blueprint: str = (make_multi_provider_call(call_type="llm", provider="openai",
                                                  input_text=project_scope_content,
                                                  config={"model": "gpt-3.5-turbo-0125",
                                                          "type_of_response": "text_only"},
                                                  kwargs={"temperature": 0.2}))
        return refined_blueprint

    @staticmethod
    def designer(project_name: str, project_description: str, design_blueprint: str) -> str:
        prompt = f'''
Project Name: {project_name}

Project Overview:

    - Project Description: Briefly outline the purpose and vision of the {project_name}. This should capture the essence of the React project and what it aims to achieve.
    
    - Project Blueprint: {design_blueprint}

Design Conceptualization Requirements:

    - Page-wise Design Descriptions: For each page outlined in the project blueprint, provide a detailed description capturing the following elements:
        * Page Functionality: Clearly describe the purpose of the page and its core functionalities. Focus on user interaction points and how they facilitate the accomplishment of user tasks.
        * Aesthetic and Theme: Detail the aesthetic or thematic direction for each page. Reference inspirations or analogous design styles, focusing on how these influence the visual and interactive aspects of the page.
        * Color Scheme and Branding: For each page, articulate how the chosen color palette and typography contribute to the overall branding and user experience. Use descriptive language to convey the visual and emotional impact of these elements.
        * Layout and Structure: Describe the layout for each page, including navigation patterns, content hierarchy, and organization of elements. Use vivid descriptions to paint a clear picture of the page layout.
        * User Interface Elements: Specify and describe unique UI elements (such as buttons, icons, sliders, animations) for each page, focusing on their design, behavior, and interaction with the user.
        * Accessibility Features: Highlight specific design considerations for each page that ensure accessibility for all users, including those with disabilities. Describe these features in detail, emphasizing how they enhance usability.

Design Deliverables:

    - Comprehensive Design Narratives: Submit detailed textual descriptions for each page, covering all the design conceptualization requirements mentioned above. These narratives should collectively paint a vivid picture of what the website will look like, providing a clear guide for the development process.

'''
        first_design_blueprint: str = (make_multi_provider_call(call_type="llm", provider="openai",
                                                  input_text=prompt,
                                                  config={"model": "gpt-3.5-turbo-0125",
                                                          "type_of_response": "text_only"},
                                                  kwargs={"temperature": 0.9}))

        refine_prompt = f'''
Given Project Name: {project_name}

Initial Design Concepts Received:
- Here, summarize or insert the design concept narratives provided from the previous stage. This should include descriptions for each page, covering functionality, aesthetics, layout, and user interface elements.

Evaluation and Refinement Criteria:

1. Alignment with Project Vision:
   - Evaluate how each page's design aligns with the overall vision and purpose of the {project_name}. Suggest adjustments to better reflect the project's goals and values.

2. Functionality and User Experience:
   - Critically assess the described functionalities and user interaction points for each page. Ensure they contribute to a seamless and intuitive user experience. Propose enhancements or simplifications where necessary.

3. Aesthetic Coherence and Branding:
   - Review the aesthetic and thematic directions for consistency across all pages. Discuss the impact of the color scheme and branding elements on user perception and suggest refinements to improve visual harmony.

4. Layout and Navigation:
   - Analyze the proposed layouts and navigation patterns for efficiency and user-friendliness. Recommend changes to optimize content hierarchy and ease of navigation.

5. Innovative UI Elements:
   - Consider the uniqueness and innovation of the specified UI elements. Offer ideas to enhance interaction design, focusing on creativity and user engagement.

6. Accessibility and Inclusivity:
   - Scrutinize the accessibility features of each page design. Propose additional considerations or improvements to ensure the website is accessible to a broader audience, including users with disabilities.

Refinement Deliverables:

- Refined Design Narratives: Based on the evaluation criteria, provide revised narratives for each page that incorporate suggested improvements. These narratives should detail the optimized design concept, ensuring it is both innovative and closely aligned with the project's vision.
'''
        refined_blueprint: str = (make_multi_provider_call(call_type="llm", provider="openai",
                                                  input_text=refine_prompt,
                                                  config={"model": "gpt-3.5-turbo-0125",
                                                          "type_of_response": "text_only"},
                                                  kwargs={"temperature": 0.2}))
        return refined_blueprint

    @staticmethod
    def create_high_level_structure(project_reqs: str, design_blueprint: str) -> Dict[str, str]:
        """
        Creates a high-level structure for the project.
        :param project_reqs: The project requirements.
        :param design_blueprint: The design blueprint.
        :return: A dictionary containing the high-level structure of the project.
        """
        prompt = f'''
Project Requirements Overview:
    {project_reqs}

Design Blueprint Summary:
    {design_blueprint}

Directory Usage Overview:

    Assets: Indicate the types of static resources you anticipate needing (e.g., images, icons).
    Components: Discuss the roles of potentially reusable components (UI elements, layout structures).
    Context: Consider if there's a need for global state management or shared context across components.
    Hooks: Mention custom hooks for shared logic or stateful functionality across components.
    Pages: Outline the main views or pages your app will feature, considering the user journey.
    Routes: Contemplate the routing strategy, especially if you foresee needing private or protected routes.
    Services: Identify external interactions, like API calls, that might be abstracted into service files.
    Utils: Point out any utility functions or helpers for common tasks across the app.

Goal: To brainstorm an ideal, high-level project structure tailored to the specific needs and design of your React frontend project. This involves understanding the potential role of each directory without committing to specific files or detailed implementations.

Instructions:

    Reflect on the project requirements and design blueprint to provide a broad view of the necessary directories and their intended purposes.
    Emphasize flexibility by noting that not every directory needs to be utilized; focus on those critical to your project's needs.
    Offer general guidance on the project's architecture, suggesting how to organize code and functionality in a scalable and maintainable way.
    Recommend considerations for ensuring the project structure supports efficient development and future growth.
    Figure out what every directory will contain or if it will be empty.
    Only talk at a high level, no need to go into the details of the files in the directories.
'''
        first_high_level_structure: str = (make_multi_provider_call(call_type="llm", provider="openai",
                                                  input_text=prompt,
                                                  config={"model": "gpt-4-0125-preview",
                                                          "type_of_response": "text_only"},
                                                  kwargs={"temperature": 0.9}))

        refine_prompt = f'''
Project Requirements Overview:
    {project_reqs}

Design Blueprint Summary:
    {design_blueprint}

Initial Structure Overview:
    {first_high_level_structure}

Refinement Goals:

    Evaluate the necessity of each proposed directory in the context of the project's specific requirements and design.
    Identify directories that may not be needed, aiming to streamline the project structure.
    Suggest enhancements or adjustments to the initial structure to improve scalability, maintainability, and development efficiency.

Instructions for Refinement:

    Reassess Each Directory:
        Based on the project's detailed requirements and design blueprint, decide if each previously mentioned directory is essential.
        Consider merging or eliminating directories that may not contribute significantly to the project's architecture or that overlap in functionality.

    Focus on Essential Directories:
        For each confirmed directory, provide a refined overview of its role within the project, emphasizing how it aligns with the project's goals.
        Highlight any changes or specific considerations that have emerged since the initial overview.

    Streamline the Structure:
        Recommend removing any directories that, upon further consideration, seem redundant or unnecessary.
        Suggest any additional directories or structural changes that could further optimize development and future scalability.

    Finalize the Project Structure:
        Based on the refinement process, outline the finalized directory structure, ensuring it is as lean and effective as possible.
        Provide a brief rationale for each included directory, summarizing its necessity and function within the project.

Output:

    A concise, refined project structure that accurately reflects the project's needs, removing any unnecessary directories and emphasizing efficiency and clarity in the organization.
    Be sure to include adequate details for each directory.
'''
        refined_structure: str = (make_multi_provider_call(call_type="llm", provider="openai",
                                                  input_text=refine_prompt,
                                                  config={"model": "gpt-4-0125-preview",
                                                          "type_of_response": "text_only"},
                                                  kwargs={"temperature": 0.4}))
        last_refine_prompt = f'''
    Requirements: {project_reqs}
    
    Structure Overview: {refined_structure}

Final Refinement Goals:

    Ensure the project structure is as simple and intuitive as possible without losing the necessary detail for implementation.
    Clarify the function and necessity of each directory within the context of the project's specific needs.
    Finalize the project architecture to facilitate a straightforward and efficient development process.

Instructions for Final Refinement:

    Evaluate for Simplicity:
        Review the refined structure to identify any areas where complexity can be reduced. Consider combining functions or further eliminating directories that are not crucial.
        Ensure the rationale behind each directory's inclusion is clear and justified by the project's requirements.

    Clarify Directory Roles:
        For each directory, provide a concise but comprehensive description of its role, including how it contributes to the project's functionality and user experience.
        Highlight any directories that are particularly important to the project's structure or that house critical features.

    Optimize for Development:
        Suggest any final adjustments to the project structure that could make the development process more efficient or reduce potential for confusion.
        Consider the workflow of the development team and how the structure supports both initial development and future maintenance or expansion.

    Document Final Structure:
        Present the finalized project directory structure, ensuring it is streamlined for simplicity while containing all necessary details for engineers.
        Include a brief explanation for the inclusion of each directory, reinforcing its importance and function within the project.

Output:

    A detailed, yet simplified, final project structure tailored to meet the project's needs efficiently. This structure should be ready for implementation, providing a clear guide for the engineering team on how to organize their work and the project's components effectively.
    Be sure to include adequate details for each directory.
'''
        refined_structure: str = (make_multi_provider_call(call_type="llm", provider="openai",
                                                  input_text=last_refine_prompt,
                                                  config={"model": "gpt-3.5-turbo-0125",
                                                          "type_of_response": "text_only"},
                                                  kwargs={"temperature": 0.1}))

        ensure_structure_aligns_with_project_reqs = f'''
Client Requirements Overview:
- {project_reqs}

Existing Project Structure:
- {refined_structure}

Refinement Objectives:
1. Enhanced Functionality: Identify areas where the project's functionality can be expanded or optimized to better meet the client's needs. Consider integrating new features or improving existing ones for efficiency and user engagement.

2. Improved User Experience: Evaluate the current user interface and user experience design. Suggest modifications that could enhance usability, accessibility, and overall satisfaction for the end-users.

3. Design and Performance Optimization: Propose changes to the project's design and structure that could improve performance, such as loading times, responsiveness, and interaction fluidity. Include considerations for mobile and desktop compatibility.

4. Technical Debt and Scalability: Assess the project's current technical foundation for potential technical debt issues. Recommend solutions for reducing complexity and ensuring the project is scalable and maintainable over time.

Refinement Plan:
- For each identified objective, provide a detailed plan on how to adjust the project's structure and components. This plan should include technical descriptions of the changes needed, potential libraries or tools to be used, and how these changes will align with the overall project goals.

Expected Outcomes:
- Outline the expected improvements in functionality, user experience, performance, and scalability as a result of the proposed refinements. Be specific about how these outcomes will meet the client's requirements and enhance the project's value.
- Ensure the structure is clear and concise. Be verbose for all descriptions of files and directories.

Deliverables:
- List the detailed technical specifications and descriptions for the refined project structure. This should include updated component diagrams, flowcharts, and descriptions of any new features or optimizations.
'''
        new_and_ensured_structure: str = (make_multi_provider_call(call_type="llm", provider="openai",
                                                    input_text=ensure_structure_aligns_with_project_reqs,
                                                    config={"model": "gpt-3.5-turbo-0125",
                                                            "type_of_response": "function_calling"}))

        jsonify_prompt = f'''
Objective: Create a JSON structure that outlines the purpose and role of specific directories within a React frontend project. This structure should serve as a clear blueprint for development, indicating what each directory is intended to house or accomplish.

Requirements:

    The JSON should contain top-level keys corresponding to the directories: assets, components, context, hooks, pages, routes, services, and utils.
    Each key's value should be a string describing the directory's purpose or role in the project. If a directory does not play a role in the project, its value should be an empty string.

Structure Overview: 
{new_and_ensured_structure}

Example JSON Structure:
{{
  "assets": "Description of the directory",
  "components": "Description of the directory",
  "context": "",
  "hooks": "Description of the directory",
  "pages": "Description of the directory",
  "routes": "Description of the directory",
  "services": "Description of the directory",
  "utils": "Description of the directory"
}}

Instructions:

    For each directory listed, provide a brief description of its intended role within the project. Consider the following aspects:
        Assets: Static resources such as images, icons, and style sheets.
        Components: Reusable UI elements and layout components.
        Context: Global state management and context providers for shared state.
        Hooks: Custom React hooks for shared logic or functionality.
        Pages: The main views or screens of the application, representing distinct parts of the user interface.
        Routes: The setup of application routing, including the mapping of URLs to pages.
        Services: Abstractions for external interactions, such as API calls and data fetching.
        Utils: Utility functions and helpers for common tasks and operations.

    Ensure the descriptions are concise yet informative enough to guide the development team in understanding the purpose and scope of each directory
    Ensure the descriptions are clear and very detailed.
'''
        json_structure: Dict[str, str] = try_json_response(
            make_multi_provider_call,
            call_type="llm", provider="openai", input_text=jsonify_prompt,
            config={"model": "gpt-3.5-turbo-0125", "type_of_response": "function_calling"})
        return json_structure

    @staticmethod
    def create_directory(directory_name: str, directory_blueprint: str) -> Dict[str, str]:
        """
        Creates a directory within the project.
        :param directory_name: Directory name.
        :param directory_blueprint: Directory blueprint.
        :return: The files created within the directory.
        """
        blueprint_for_dir_creation_prompt = f'''
Objective: Create a detailed text-based blueprint of a specified subdirectory within a React project. The blueprint should focus on the identification and description of necessary files, assuming there will be no imports in any of the files. The goal is to outline the structure and purpose of each file, enhancing the planning phase of development.

Directory Name: {directory_name}
Directory Description: {directory_blueprint}

Instructions:

    Subdirectory Description Input: Start with a detailed description of the subdirectory's intended functionality within the React project. This should include the feature it will support, any specific components or utilities it will contain, and the overall purpose within the application's architecture.

    Blueprint Generation:
        File Identification: Based on the subdirectory's description, list all the necessary files that need to be created. Focus solely on Javascript files and DO NOT suggest the creation of more directories.
        File Description: For each identified file, generate a brief description of its purpose and functionality. Include what each file will accomplish and any specific components, hooks, or utilities it might define.
        Remember, no imports or external dependencies should be assumed or included in the file descriptions.

    Format: Present the blueprint as follows:
        Subdirectory Name: [Name of the Subdirectory]
        Subdirectory Description: [Description of its purpose and functionality]
        Files:
            File Name 1: Description of its purpose and functionality.
            File Name 2: Description of its purpose and functionality.
            [...]

    Assumptions: It's assumed that the subdirectory is part of a larger React project structure, focusing on a specific feature or functionality. Every file is assumed to have no imports or external dependencies.
'''
        first_directory: str = (make_multi_provider_call(call_type="llm", provider="openai",
                                                  input_text=blueprint_for_dir_creation_prompt,
                                                  config={"model": "gpt-3.5-turbo-0125",
                                                          "type_of_response": "text_only"},
                                                  kwargs={"temperature": 0.5}))

        refine_prompt = f'''
Objective: Generate a concise, actionable blueprint for a React project subdirectory, focusing on file creation with clear, purpose-driven descriptions. This streamlined approach aims to facilitate the development process by outlining essential files without assuming imports.

Directory Name: {directory_name}
Initial Blueprint: {first_directory}

Instructions:

    Input Description: Begin with a concise description of the subdirectory's role in the React project. Highlight key functionalities, components, or utilities it aims to provide.

    Blueprint Simplification:
        Identify Essential Files: List only the necessary files, focusing on only .js. Exclude further directories to maintain simplicity.
        Merge Similar Functions: Where possible, combine files with overlapping functionalities to reduce redundancy. For example, utility functions for API calls can be grouped into a single file.
        Clarify File Purposes: For each file, provide a succinct description that captures its core functionality and role within the subdirectory.

    Blueprint Format:
        Subdirectory Name: [Insert Subdirectory Name]
        Essential Files: List each file with a brief description of its functionality and purpose.

    Assumptions: The blueprint assumes a modular approach, focusing on scalability and ease of integration within the broader React application framework.
'''
        refined_directory: str = (make_multi_provider_call(call_type="llm", provider="openai",
                                                  input_text=refine_prompt,
                                                  config={"model": "gpt-3.5-turbo-0125",
                                                          "type_of_response": "text_only"},
                                                  kwargs={"temperature": 0.2}))

        create_files_prompt = f'''
Objective: Transform the refined blueprint of a React project subdirectory into a JSON object. Each key in the JSON object should correspond to a JavaScript file name within the subdirectory, and the associated value should describe the file's functionality and purpose.

Refined Blueprint: {refined_directory}

Instructions:

    Blueprint Input: Start with the output of the refined React subdirectory blueprint, which lists essential files and their descriptions.

    Conversion to JSON:
        JSON Structure: Create a JSON object where each entry consists of a key-value pair.
        Key Naming: Use the JavaScript file names (with the file extension) as keys in the JSON object.
        Value Description: The value for each key should be a string describing the file's core functionality and role within the subdirectory.

    JSON Formatting:
        Ensure the JSON object is correctly formatted, with proper use of quotes and commas.
        Validate the JSON to check for syntax errors before finalizing.
        Ensure the JSON has strings for both keys and values, with no nested objects or arrays.
        Be as verbose as needed for all descriptions of files and directories.
'''
        files_created: Dict[str, str] = try_json_response(
            make_multi_provider_call,
            call_type="llm", provider="openai", input_text=create_files_prompt,
            config={"model": "gpt-3.5-turbo-0125", "type_of_response": "function_calling"})

        return files_created

    @staticmethod
    def create_component_code(description_of_code: str) -> str:
        """
        Creates the code for a component.
        :param description_of_code: The description of the component's functionality.
        :return: The code for the component.
        """
        prompt = f'''
Objective: Create a comprehensive React component file based on the provided description.

Input Description:
- {description_of_code}

Output Specifications:

    Component Setup: Start with importing React, necessary hooks, and other dependencies.
    Props Definition: Define the component function with props parameter and destructure the props as needed.
    Function Implementations: Implement the specified event handlers and functions within the component.
    JSX Structure: Construct the JSX layout according to the described structure and include any child components.
    Styling: DO NOT CREATE STYLES. They will be added later.
    Export Statement: Export the component at the end of the file.
'''
        component_code2: str = make_multi_provider_call(call_type="llm", provider="openai",
                                                 input_text=prompt,
                                                 config={"model": "gpt-3.5-turbo-0125",
                                                         "type_of_response": "code_only"},
                                                 kwargs={"temperature": 0.7})
        component_code: str = extract_code_from_output(component_code2)
        return component_code

    @staticmethod
    def create_css_code(description_of_code: str, component_code: str) -> str:
        """
        Creates the code for css.
        :param description_of_code: The description of the component's functionality.
        :param component_code: The code for the component.
        :return: The code for the css file.
        """
        prompt = f'''
Objective: Create a CSS or styled-components file for a React component based on the provided description and component requirements.


Input Description:

    Description of the code: {description_of_code}
    Component Code: {component_code}

Output Specifications:

    Style Definitions:
        Define classes corresponding to the component's elements with detailed style properties.
    Colors and Typography: Implement the color scheme and typography as described, using variables for consistency if necessary.
    Layout and Spacing: Ensure the layout, margin, padding, and positioning align with the described design.
    Responsiveness: Include media queries or responsive design solutions as required.
    Special Effects: Add any specified animations, transitions, or visual effects.
    Exporting:
        Ensure the file is ready to be linked or imported into the React component.

'''
        css_code_output: str = make_multi_provider_call(call_type="llm", provider="openai",
                                                        input_text=prompt,
                                                        config={"model": "gpt-3.5-turbo-0125",
                                                                "type_of_response": "code_only"},
                                                        kwargs={"temperature": 0.7})
        css_code: str = extract_code_from_output(css_code_output)
        return css_code

    @staticmethod
    def create_js_test_code(description_of_code: str, component_code: str) -> str:
        """
        Creates the code for the js test.
        :param description_of_code: The description of the component's functionality.
        :param component_code: The code for the component.
        :return: The code for the test file.
        """
        prompt = f'''
Title: Generate a Test File for a React Component Using Jest and React Testing Library

Objective: Create a test file for a specified React component that covers its functionality, props, and user interactions using Jest and React Testing Library.

Input Description:

    Description of the code: {description_of_code}
    Component Code: {component_code}

Output Specifications:

    Describe Blocks: Use describe blocks to group tests by functionality or component features.
    Test Cases:
        Write test cases using it or test to describe what each test aims to verify.
        Include tests for rendering the component with various props.
        Test user interactions using fireEvent or userEvent and assert expected outcomes.
        Check for conditional rendering and state changes.
        Mock any external dependencies or API calls as necessary.
    Assertions: Use assertions to check if the component behaves as expected under various conditions (e.g., expect statements).
    Cleanup: Ensure tests clean up after themselves to prevent side effects between tests.
'''
        test_code_output: str = make_multi_provider_call(call_type="llm", provider="openai",
                                                        input_text=prompt,
                                                        config={"model": "gpt-3.5-turbo-0125",
                                                                "type_of_response": "code_only"},
                                                        kwargs={"temperature": 0.7})
        test_code: str = extract_code_from_output(test_code_output)
        return test_code

    @staticmethod
    def create_js_view(description_of_view: str, component_code: List[str]) -> str:
        """
        Creates the code for a view.
        :param description_of_view: The description of the view's functionality.
        :param component_code: All the components that will be used in the view.
        :return: The code for the view file.
        """
        prompt = f'''
Title: Generate a JavaScript View

Objective: Create a JavaScript (JS) view file based on the provided description, incorporating given React components and specifying their arrangement and functionality within the view.

Input Description:
    Description of the view: {description_of_view}
    All the components that can be used in the view: {component_code}

Output Specifications:

    Component Setup: Define a functional component for the view, setting up any state or context needed.
    Layout Implementation: Arrange the imported components according to the specified layout, passing necessary props and handling any required data flow between them.
    Event Handling: Implement functions to handle specified user interactions and events within the view.
    Styling: Apply the described styling guidelines to the view, ensuring consistency with the overall theme.
    Additional Features: Include any routing, data fetching, or context provision as required by the view's description.
    Export Statement: Export the view component for use in the application.
'''
        test_code_output: str = make_multi_provider_call(call_type="llm", provider="openai",
                                                        input_text=prompt,
                                                        config={"model": "gpt-3.5-turbo-0125",
                                                                "type_of_response": "code_only"},
                                                        kwargs={"temperature": 0.7})
        test_code: str = extract_code_from_output(test_code_output)
        return test_code

    