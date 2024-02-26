from typing import Callable
from global_code.helpful_functions import CustomError
from prompts.cleaning_outputs import clean_and_convert_llm_response


def try_json_response(api_call: Callable, *args, **kwargs) -> dict:
    """
    Tries to call the function and return the JSON response.
    If the attempt fails three times, it's probably a bad prompt. Does not deal with the api call.
    The code that tries to get the JSON is very bad.
    CAN RAISE AN ERROR
    :param api_call: The api call to the LLM
    :param args: the arguments to pass to the function
    :param kwargs: the keyword arguments to pass to the function
    :return: the JSON response from the function
    """
    for _ in range(3):
        try:
            response: str = api_call(*args, **kwargs)  # This is the api call to an LLM
            converted_json: dict = clean_and_convert_llm_response(response)
            return converted_json
        except CustomError:
            continue
        except Exception as e:
            raise CustomError("Prompt Failed")
    raise CustomError("Prompt Failed")
