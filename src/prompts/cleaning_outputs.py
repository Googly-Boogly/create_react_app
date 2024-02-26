import json
import os

from global_code.helpful_functions import CustomError, create_logger_error, log_it
logger = create_logger_error(file_path=os.path.abspath(__file__), name_of_log_file='cleaning_llm_outputs',
                                 log_to_console=True, log_to_file=True)


def clean_and_convert_llm_response(response: str) -> dict:
    """
    Extracts the JSON portion of the LLM response and converts it to a dictionary.
    :param response: the response from an LLM
    :return: the JSON in the response
    """
    # More robustly strip the markdown code block delimiters and potential trailing spaces or new lines
    try:
        output = json.loads(response)
        return output
    except Exception as e:
        pass
    try:
        start_index = response.index('{')
        end_index = response.rindex('}') + 1
        json_str = response[start_index:end_index]
        return json.loads(json_str)
    except Exception as e:
        log_it(logger=logger, error=None, custom_message=f"JSON msg that broke: {response}", log_level="info")
        raise CustomError("soft_error")


def extract_code_from_output(lm_output: str) -> str:
    """
    Extracts the code block from the LLM output.
    :param lm_output: What the llm said
    :return: the code block
    """

    # Define start and end markers
    start_marker = "```python"
    end_marker = "```"
    # lm_output = lm_output + "# End of code block"
    # Find the indices for the start and end of the code block
    start_index = lm_output.find(start_marker) + len(start_marker)
    end_index = lm_output.find(end_marker, start_index)

    # Extract the code block, stripping any leading/trailing whitespace or newlines
    code_block = lm_output[start_index :end_index].strip()
    code_block = "\n" + code_block + "\n"
    return code_block

