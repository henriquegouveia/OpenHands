import json
import time
from typing import Optional, Dict, Any, Union, List
import requests
from openhands.core.logger import openhands_logger as logger
from litellm import ModelResponse, Usage, PromptTokensDetails

def flow_ai_completion(
    model: str,
    messages: list,
    api_key: Optional[str] = None,
    base_url: Optional[str] = "https://flow.ciandt.com/ai-orchestration-api",
    api_version: Optional[str] = None,
    max_tokens: Optional[int] = None,
    stream: bool = False,
    stop: Optional[Union[str, List[str]]] = None,
    functions: Optional[List[Dict[str, Any]]] = None,
    function_call: Optional[Union[str, Dict[str, Any]]] = None,
    timeout: Optional[int] = None,
    **kwargs: Any
) -> ModelResponse:
    url = f"https://flow.ciandt.com/ai-orchestration-api/v1/openai/chat/completions"
    
    payload = {
        "model": "o3-mini",
        "messages": messages,
        "stream": stream,
        "stop": stop,
        "function_call": function_call,
    }
    # Add any additional parameters from kwargs
    for key, value in kwargs.items():
        if value is not None:
            payload[key] = value
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "FlowTenant": "abi",
        "FlowAgent": "openhands",
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=timeout)
        response.raise_for_status()
    except requests.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Log the error
        print(f'Response content: {response.content}')  # Log the response content
        raise
    except Exception as err:
        print(f'Other error occurred: {err}')  # Log other errors
        raise

    result = response.json()

    log('info', f"Response: {json.dumps(result)}")
    
    # Transform the result to match OpenAI's format
    return ModelResponse(
        id=result.get("id", ""),
        object="chat.completion",
        created=result.get("created", int(time.time())),
        model=result.get("model", model),
        choices=[
            {
                "index": choice.get("index", 0),
                "message": {
                    "role": choice["message"].get("role", "assistant"),
                    "content": choice["message"].get("content", ""),
                    "refusal": choice["message"].get("refusal", None),
                    "tool_calls": choice["message"].get("tool_calls", [])
                },
                "finish_reason": choice.get("finish_reason", "stop"),
                "content_filter_results": choice.get("content_filter_results", {}),
                "logprobs": choice.get("logprobs", None)
            } for choice in result.get("choices", [])
        ],
        usage=Usage(
            completion_tokens=result.get("usage", {}).get("completion_tokens", 0),
            completion_tokens_details=result.get("usage", {}).get("completion_tokens_details", {}),
            prompt_tokens=result.get("usage", {}).get("prompt_tokens", 0),
            prompt_tokens_details=PromptTokensDetails(
                cached_tokens=result.get("usage", {}).get("prompt_tokens_details", {}).get("cached_tokens", 0)
            ),
            total_tokens=result.get("usage", {}).get("total_tokens", 0)
        ),
        prompt_filter_results=result.get("prompt_filter_results", []),
        system_fingerprint=result.get("system_fingerprint", "")
    )

def log(level: str, message: str, extra: dict | None = None) -> None:
    """Logs a message to the agent controller's logger."""
    message = f'[Agent Controller] {message}'
    getattr(logger, level)(message, extra=extra, stacklevel=2)
    

def flow_bedrock_completion(
    messages: list,
    api_key: Optional[str] = None,
    base_url: Optional[str] = "https://flow.ciandt.com/ai-orchestration-api",
    anthropic_version: Optional[str] = "bedrock-2023-05-31",
    max_tokens: Optional[int] = 1000,
    top_k: Optional[int] = 250,
    stop_sequences: Optional[List[str]] = None,
    temperature: Optional[float] = 1.0,
    top_p: Optional[float] = 0.999,
    allowed_models: Optional[List[str]] = None,
    timeout: Optional[int] = None,
    **kwargs: Any
) -> Dict[str, Any]:
    url = f"{base_url}/v1/bedrock/invoke"

     # Adjust the type field in the messages content
    for message in messages:
        if "content" in message and isinstance(message["content"], list):
            for content_item in message["content"]:
                if "type" in content_item:
                    content_item["type"] = "custom"  # Replace 'text' with an expected tag like 'custom'
    
    payload = {
        "messages": messages,
        "anthropic_version": 'bedrock-2023-05-31',
        "max_tokens": max_tokens,
        "top_k": top_k,
        "stop_sequences": stop_sequences or [],
        "temperature": 0.6,
        "top_p": top_p or 0.999,
        "allowedModels": allowed_models or ["anthropic.claude-37-sonnet"],
        **kwargs,
    }

    print("Payload:", json.dumps(payload, indent=2))  # Debugging line to check the payload

    # Add any additional parameters from kwargs
    for key, value in kwargs.items():
        if value is not None:
            payload[key] = value
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "FlowTenant": "pepsico",
        "FlowAgent": "flow-openhands",
        "FlowOperationId": "henriquegouveia",
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=timeout)
        response.raise_for_status()
    except requests.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Log the error
        print(f'Response content: {response.content}')  # Log the response content
        raise
    except Exception as err:
        print(f'Other error occurred: {err}')  # Log other errors
        raise

    result = response.json()

    log('info', f"Response: {json.dumps(result)}")
    
    return result