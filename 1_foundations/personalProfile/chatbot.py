"""
Chatbot functionality with OpenAI function calling.
"""
from pathlib import Path
from typing import List, Dict
from dotenv import load_dotenv
from openai import OpenAI
from logging import getLogger

from tools import TOOLS, handle_tool_calls
from personal_data import get_system_prompt, NAME

logger = getLogger(__name__)

# Load environment variables
env_paths = [
    Path("../../.env"),
    Path("/Users/kramkrishnaachary/learning/github/agents/.env"),
    Path(".env"),
]

for path in env_paths:
    if path.exists():
        load_dotenv(dotenv_path=path, override=True)
        break
else:
    load_dotenv(override=True)


class PersonalChatbot:
    """
    Chatbot that acts as a personal representative with function calling capabilities.
    """
    
    def __init__(self, name: str = NAME, model: str = "gpt-4o-mini"):
        """
        Initialize the chatbot.
        
        Args:
            name: The name of the person the chatbot represents
            model: The OpenAI model to use
        """
        self.name = name
        self.model = model
        self.client = OpenAI()  # Uses OPENAI_API_KEY from environment
        self.system_prompt = get_system_prompt(name)
        logger.info(f"Initialized PersonalChatbot for {name}")
    
    def chat(self, message: str, history: List[Dict[str, str]]) -> str:
        """
        Process a chat message with function calling support.
        
        Args:
            message: The user's message
            history: List of previous messages in the conversation
        
        Returns:
            The assistant's response text
        """
        # Build messages list with system prompt, history, and current message
        messages = [
            {"role": "system", "content": self.system_prompt}
        ] + history + [
            {"role": "user", "content": message}
        ]
        
        done = False
        while not done:
            # Call the LLM with tools
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=TOOLS
            )
            
            finish_reason = response.choices[0].finish_reason
            
            # If the LLM wants to call a tool, execute it
            if finish_reason == "tool_calls":
                message_obj = response.choices[0].message
                tool_calls = message_obj.tool_calls
                results = handle_tool_calls(tool_calls)
                
                # Add the assistant's message (with tool calls) and tool results to conversation
                messages.append(message_obj)
                messages.extend(results)
            else:
                done = True
        
        return response.choices[0].message.content


def create_chat_function(name: str = NAME, model: str = "gpt-4o-mini"):
    """
    Create a chat function compatible with Gradio ChatInterface.
    
    Args:
        name: The name of the person the chatbot represents
        model: The OpenAI model to use
    
    Returns:
        A chat function that takes (message, history) and returns response
    """
    chatbot = PersonalChatbot(name=name, model=model)
    
    def chat(message: str, history: List[Dict[str, str]]) -> str:
        return chatbot.chat(message, history)
    
    return chat

