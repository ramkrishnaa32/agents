"""
Helper functions for interacting with OpenAI API.
"""
from openai import OpenAI
from typing import Optional
from logging import getLogger

logger = getLogger(__name__)


class OpenAIHelper:
    """
    Helper class to interact with the OpenAI API using the OpenAI Python client.
    
    Example:
        helper = OpenAIHelper()  # Uses credentials from .env
        response = helper.get_response(messages=[{"role": "user", "content": "Hello"}])
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the OpenAI client.
        
        Args:
            api_key: OpenAI API key. If None, will try to load from credentials module.
        """
        if api_key is None:
            try:
                from credentials import get_openai_key
                api_key = get_openai_key()
            except ImportError:
                raise ImportError(
                    "credentials module not found. Either provide api_key or ensure credentials.py exists."
                )
            except ValueError as e:
                raise ValueError(f"Failed to load OpenAI API key: {e}")
        
        self.client = OpenAI(api_key=api_key)
        logger.info("OpenAI client initialized successfully")

    def get_response(
        self, 
        messages: list[dict], 
        model: str = "gpt-4o-mini",
        temperature: float = 1.0,
        max_tokens: Optional[int] = None
    ):
        """
        Get a response from the OpenAI API.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            model: Model to use (default: "gpt-4o-mini")
            temperature: Sampling temperature (default: 1.0)
            max_tokens: Maximum tokens in response (optional)
        
        Returns:
            ChatCompletion object from OpenAI API
        
        Raises:
            Exception: If API call fails
        """
        if not messages:
            raise ValueError("messages list cannot be empty")
        
        try:
            params = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
            }
            if max_tokens is not None:
                params["max_tokens"] = max_tokens
            
            response = self.client.chat.completions.create(**params)
            logger.debug(f"Successfully got response from {model}")
            return response
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {e}")
            raise

    def get_response_text(
        self,
        messages: list[dict],
        model: str = "gpt-4o-mini",
        temperature: float = 1.0,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Get just the text content from the OpenAI API response.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            model: Model to use (default: "gpt-4o-mini")
            temperature: Sampling temperature (default: 1.0)
            max_tokens: Maximum tokens in response (optional)
        
        Returns:
            String content of the assistant's message
        """
        response = self.get_response(messages, model, temperature, max_tokens)
        return response.choices[0].message.content


# Backward compatibility alias
openaiHelper = OpenAIHelper

