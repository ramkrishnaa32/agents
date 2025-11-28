"""
Credentials management module for accessing API keys and other secrets.
All credentials are loaded from environment variables via .env file.
"""
import os
from dotenv import load_dotenv
from logging import getLogger

logger = getLogger(__name__)

# Load environment variables from .env file
# override=True ensures that environment variables take precedence
load_dotenv(override=True)


def get_openai_key() -> str:
    """Get OpenAI API key from environment variables."""
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError(
            "OPENAI_API_KEY is not set. Please create a .env file with OPENAI_API_KEY=your_key_here"
        )
    return key


def get_anthropic_key() -> str:
    """Get Anthropic API key from environment variables."""
    key = os.getenv("ANTHROPIC_API_KEY")
    if not key:
        raise ValueError(
            "ANTHROPIC_API_KEY is not set. Please create a .env file with ANTHROPIC_API_KEY=your_key_here"
        )
    return key


def get_langsmith_key() -> str | None:
    """Get LangSmith API key from environment variables (optional)."""
    return os.getenv("LANGSMITH_API_KEY")


def get_sendgrid_key() -> str | None:
    """Get SendGrid API key from environment variables (optional)."""
    return os.getenv("SENDGRID_API_KEY")


def get_polygon_key() -> str | None:
    """Get Polygon API key from environment variables (optional)."""
    return os.getenv("POLYGON_API_KEY")


def get_env_var(key: str, required: bool = False, default: str | None = None) -> str | None:
    """
    Generic function to get any environment variable.
    
    Args:
        key: The environment variable name
        required: If True, raises ValueError if key is not found
        default: Default value if key is not found and not required
    
    Returns:
        The environment variable value or default/None
    """
    value = os.getenv(key, default)
    if required and not value:
        raise ValueError(
            f"{key} is not set. Please create a .env file with {key}=your_value_here"
        )
    return value


# Convenience function to check if all required credentials are set
def check_required_credentials(keys: list[str]) -> dict[str, bool]:
    """
    Check which required credentials are set.
    
    Args:
        keys: List of environment variable names to check
    
    Returns:
        Dictionary mapping key names to boolean (True if set, False if not)
    """
    return {key: bool(os.getenv(key)) for key in keys}

