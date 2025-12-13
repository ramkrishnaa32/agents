"""
Pushover notification functionality for recording user interactions.
"""
import os
import requests
from pathlib import Path
from dotenv import load_dotenv
from logging import getLogger

logger = getLogger(__name__)

# Load environment variables
env_paths = [
    Path("../../.env"),  # Relative from personalProfile location
    Path("/Users/kramkrishnaachary/learning/github/agents/.env"),  # Absolute path
    Path(".env"),  # Current directory
]

for path in env_paths:
    if path.exists():
        load_dotenv(dotenv_path=path, override=True)
        logger.info(f"Loaded .env from: {path}")
        break
else:
    load_dotenv(override=True)  # Fallback to default behavior

# Initialize Pushover credentials
pushover_user = os.getenv("PUSHOVER_USER")
pushover_token = os.getenv("PUSHOVER_TOKEN")
pushover_url = "https://api.pushover.net/1/messages.json"


def push(message: str) -> None:
    """
    Send a Pushover notification.
    
    Args:
        message: The message to send via Pushover
    """
    global pushover_user, pushover_token
    
    # Reload variables if they're None
    if pushover_user is None or pushover_token is None:
        for path in env_paths:
            if path.exists():
                load_dotenv(dotenv_path=path, override=True)
                break
        
        pushover_user = os.getenv("PUSHOVER_USER")
        pushover_token = os.getenv("PUSHOVER_TOKEN")
    
    if pushover_user is None or pushover_token is None:
        logger.warning(f"Pushover credentials not available. Message: {message}")
        print(f"Warning: Pushover credentials not available. Message: {message}")
        return
    
    print(f"Push: {message}")
    payload = {"user": pushover_user, "token": pushover_token, "message": message}
    try:
        requests.post(pushover_url, data=payload)
        logger.debug(f"Pushover notification sent: {message[:50]}...")
    except Exception as e:
        logger.error(f"Error sending Pushover notification: {e}")
        print(f"Error sending Pushover notification: {e}")

