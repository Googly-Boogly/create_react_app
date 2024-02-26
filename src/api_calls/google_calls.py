# import google.cloud.language_v1 as language
from typing import Dict, Any, Callable


def handle_google_call(call_type: str, input_text: str, config: Dict[str, Any], tools: Dict[str, Callable],
                        **kwargs) -> str:
    if call_type != "llm":
        raise ValueError("Google provider currently only supports LLM calls")

    # client = language.LanguageServiceClient()
    # document = language.Document(content=input_text, type_=language.Document.Type.PLAIN_TEXT)
    #
    # # Example LLM request customization (see Google NLP API docs for more options)
    # features = {"extract_syntax": True, "extract_entities": True}
    #
    # response = client.analyze_entities(document=document, features=features)
    #
    # # TODO: Extract and format desired results from 'response' before returning
    return "Google LLM Response (Modify based on the results you want)"