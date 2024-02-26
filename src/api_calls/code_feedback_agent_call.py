from openai import OpenAI
from global_code.singleton import State
import openai


def code_feedback_agent_call(initial_prompt: str, code: str) -> str:
    """
    Create the agent Needs to have access too tools.
    Will need to make sure that the code calls the correct tool.
    :param initial_prompt:
    :param tools: List of tools that the agent will have access too
    :param code: the code that the agent will check
    :return: the response
    """
    tools = [{
                "type": "function",
                "function": {
                    "name": "response",
                    "description": "Will communicate to the programmer if the code looks good or not",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "what_to_change": {
                                "type": "string",
                                "description": "Description to the programmer of what to change"
                            },
                            "looks_good_or_not": {
                                "type": "string",
                                "description": "If the code looks good or not ONLY INCLUDE 'TRUE' OR 'FALSE'"
                            }
                        },
                    },
                    "required": ["looks_good_or_not"]
                }
        },
        {"type": "code_interpreter"}]
    client = OpenAI(api_key=State.config['OPENAI']['API_KEY'])
    completion = client.chat.completions.create(
        messages=[{"role": "user", "content": "Check to see if the code looks good"}],
        model="gpt-4-turbo-preview",
        tools=tools,
        tool_choice="auto"
    )
    print(completion)
    return completion