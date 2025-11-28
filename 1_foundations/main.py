from helperFunctions import openaiHelper
import os
from dotenv import load_dotenv
load_dotenv(override=True)


from logging import getLogger
logger = getLogger(__name__)


def main():

    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        logger.error("OPENAI_API_KEY is not set")
        raise ValueError("OPENAI_API_KEY is not set")

    prompt = "Help me to pick a business that is worth exploring for an agentic AI opportunity"
    content = "You are a helpful assistant, you are given a prompt and you need to help the user to pick a business are that worth exploring for investing for an  agentic AI opportunity"
    messages = [
        {
            "role": "system",
            "content": content
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
    openai_helper = openaiHelper(openai_api_key)
    response = openai_helper.get_response(messages=messages)
    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()