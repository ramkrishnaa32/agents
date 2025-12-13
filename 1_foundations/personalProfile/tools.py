"""
Tool definitions and handlers for OpenAI function calling.
"""
import json
from typing import List, Dict, Any
from logging import getLogger

from pushover import push

logger = getLogger(__name__)


def record_user_details(email: str, name: str = "Name not provided", notes: str = "not provided") -> Dict[str, str]:
    """
    Record that a user is interested in being in touch and provided an email address.
    
    Args:
        email: The email address of this user
        name: The user's name, if they provided it
        notes: Any additional information about the conversation that's worth recording
    
    Returns:
        Dictionary with "recorded": "ok"
    """
    push(f"Recording interest from {name} with email {email} and notes {notes}")
    return {"recorded": "ok"}


def record_unknown_question(question: str) -> Dict[str, str]:
    """
    Record any question that couldn't be answered.
    
    Args:
        question: The question that couldn't be answered
    
    Returns:
        Dictionary with "recorded": "ok"
    """
    push(f"Recording {question} asked that I couldn't answer")
    return {"recorded": "ok"}


# Tool definitions in OpenAI function calling format
RECORD_USER_DETAILS_JSON = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address of this user"
            },
            "name": {
                "type": "string",
                "description": "The user's name, if they provided it"
            },
            "notes": {
                "type": "string",
                "description": "Any additional information about the conversation that's worth recording to give context"
            }
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

RECORD_UNKNOWN_QUESTION_JSON = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question that couldn't be answered"
            },
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

# Tools array for OpenAI API
TOOLS = [
    {"type": "function", "function": RECORD_USER_DETAILS_JSON},
    {"type": "function", "function": RECORD_UNKNOWN_QUESTION_JSON}
]

# Tool registry for dynamic lookup
TOOL_REGISTRY = {
    "record_user_details": record_user_details,
    "record_unknown_question": record_unknown_question,
}


def handle_tool_calls(tool_calls: List[Any]) -> List[Dict[str, Any]]:
    """
    Handle tool calls from OpenAI API by executing the appropriate functions.
    
    Args:
        tool_calls: List of tool call objects from OpenAI API
    
    Returns:
        List of tool result dictionaries formatted for OpenAI API
    """
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        logger.info(f"Tool called: {tool_name}")
        print(f"Tool called: {tool_name}", flush=True)
        
        # Dynamically look up and call the tool function
        tool = TOOL_REGISTRY.get(tool_name)
        if tool:
            result = tool(**arguments)
        else:
            logger.warning(f"Unknown tool: {tool_name}")
            result = {"error": f"Unknown tool: {tool_name}"}
        
        results.append({
            "role": "tool",
            "content": json.dumps(result),
            "tool_call_id": tool_call.id
        })
    
    return results

