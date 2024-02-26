from typing import Dict, Callable, Any, Optional
from gold.api_calls.google_calls import handle_google_call
from gold.api_calls.mixtral_calls import handle_mixtral_call
from gold.api_calls.openai_call import handle_openai_call


def make_multi_provider_call(call_type: str,
                             provider: str,
                             input_text: str,
                             config: Dict[str, Any],
                             tools: Optional[Dict[str, Callable]] = None,
                             **kwargs) -> Any:
    """
    A versatile function to handle diverse API calls to LLMs, RAGs, and tools
    across different providers (Google, OpenAI, etc.).

    Args:
        call_type:  Specifies the type of request (e.g., "llm", "rag", "tool")
        provider:   Indicates the provider (e.g., "google", "openai", "mixtral")
        input_text: The primary text input for the call
        config:     Key-value pairs for provider-specific settings
                    (e.g., API keys, model names, endpoint URLs).
        tools:      A dictionary mapping tool names to callable functions that
                    implement the tool's logic.
        **kwargs:   Additional keyword arguments for finer control of the API call.

    Returns:
        str: The response from the executed API call.
    """

    # Provider-Specific Logic
    if provider == "google":
        response = handle_google_call(call_type, input_text, config, tools, **kwargs)
    elif provider == "openai":
        response = handle_openai_call(call_type, input_text, config, tools, **kwargs)
    elif provider == "mixtral":
        response = handle_mixtral_call(call_type, input_text, config, tools, **kwargs)
    else:
        raise ValueError(f"Unsupported provider: {provider}")

    return response