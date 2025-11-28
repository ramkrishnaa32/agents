from helperFunctions import OpenAIHelper
from logging import getLogger

logger = getLogger(__name__)


def main():
    """Main function to demonstrate OpenAI helper usage."""
    # Initialize helper (automatically loads credentials from .env)
    helper = OpenAIHelper()

    prompt = "Help me to pick a business that is worth exploring for an agentic AI opportunity"
    system_content = (
        "You are a helpful assistant. You are given a prompt and you need to help "
        "the user to pick a business area that is worth exploring for investing in "
        "an agentic AI opportunity."
    )
    
    messages = [
        {"role": "system", "content": system_content},
        {"role": "user", "content": prompt}
    ]
    
    # Get response text directly
    response_text = helper.get_response_text(messages=messages)
    print(response_text)

if __name__ == "__main__":
    main()