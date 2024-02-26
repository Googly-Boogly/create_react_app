import os
from global_code.helpful_functions import CustomError


def change_js_file(file_path: str, type_of_change: str, rewrite_or_append: bool, new_string: str):
    """
    Modify a JS file to either change the imports section or the code section.
    :param file_path: The path to the JS file.
    :param type_of_change: Either 'import' or 'code', or 'function'
    :param rewrite_or_append: Either True for rewrite or False for append.
    :param new_string: The change to make.
    """
    # Read the original file content
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Define markers for import and code sections
    import_start_marker = '// IMPORTS\n'
    import_end_marker = '// END IMPORTS\n'
    code_start_marker = '// CODE\n'
    code_end_marker = '// END CODE\n'
    function_start_marker = '// FUNCTION CODE\n'
    function_end_marker = '// END FUNCTION CODE\n'
    # Initialize variables to track the positions of the sections
    import_start_pos, import_end_pos, code_start_pos, code_end_pos, function_start_pos, function_end_pos = 0, 0, 0, 0, 0, 0

    # Find the positions of the import and code sections
    for i, line in enumerate(lines):
        if line == import_start_marker:
            import_start_pos = i
        elif line == import_end_marker:
            import_end_pos = i
        elif line == code_start_marker:
            code_start_pos = i
        elif line == code_end_marker:
            code_end_pos = i
        elif line == function_start_marker:
            function_start_pos = i
        elif line == function_end_marker:
            function_end_pos = i

    # Perform the required operation based on type_of_change and rewrite_or_append
    if type_of_change == 'import':
        if rewrite_or_append:  # Rewrite the entire import section
            lines = lines[:import_start_pos + 1] + [new_string + '\n'] + lines[import_end_pos:]
        else:  # Append to the import section
            lines.insert(import_end_pos, new_string + '\n')
    elif type_of_change == 'code':
        if rewrite_or_append:  # Rewrite the entire code section
            lines = lines[:code_start_pos + 1] + [new_string + '\n'] + lines[code_end_pos:]
        else:  # Append to the code section
            lines.insert(code_end_pos, new_string + '\n')
    elif type_of_change == 'function':
        if rewrite_or_append:  # Rewrite the entire code section
            lines = lines[:function_start_pos + 1] + [new_string + '\n'] + lines[function_end_pos:]
        else:  # Append to the code section
            lines.insert(function_end_pos, new_string + '\n')
    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)

# Commenting out function calls to adhere to instructions
# change_python_file('example.py', 'import', False, 'import numpy as np')


def read_js_file(file_path: str, what_to_read: str) -> str:
    """
    Read a JS file to either get the code or the imports section, or the whole thing.
    :param file_path: The path to the JS file.
    :param what_to_read: Either 'code', 'imports', 'all'
    :return: The specified section of the file as a string.
    """
    # Read the entire file content
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Define markers for import and code sections
    import_start_marker = '// IMPORTS\n'
    import_end_marker = '// END IMPORTS\n'
    code_start_marker = '// CODE\n'
    code_end_marker = '// END CODE\n'

    # Initialize variables to track the positions of the sections
    import_start_pos, import_end_pos, code_start_pos, code_end_pos = 0, 0, 0, 0

    # Find the positions of the import and code sections
    for i, line in enumerate(lines):
        if line == import_start_marker:
            import_start_pos = i
        elif line == import_end_marker:
            import_end_pos = i
        elif line == code_start_marker:
            code_start_pos = i
        elif line == code_end_marker:
            code_end_pos = i

    # Extract the specified section based on what_to_read
    if what_to_read == 'imports':
        section_lines = lines[import_start_pos + 1:import_end_pos]
    elif what_to_read == 'code':
        section_lines = lines[code_start_pos + 1:code_end_pos]
    elif what_to_read == 'all':
        section_lines = lines
    else:
        raise CustomError("Incorrect value for what_to_read")

    # Convert the list of lines back into a single string
    return ''.join(section_lines)


def create_base_js_file(file_path: str, description: str = '', code: str = '', imports: str = ''):
    base_file = f'''
////////////////////////////////////////////////////////////////////////////////////////
// Telomere

// IMPORTS

{imports}

// END IMPORTS

// CODE

{code}

// END CODE
/*
// DESCRIPTION

{description}

// END DESCRIPTION
*/

// Telomere
////////////////////////////////////////////////////////////////////////////////////////
'''
    with open(file_path, 'w') as file:
        file.write(base_file)
