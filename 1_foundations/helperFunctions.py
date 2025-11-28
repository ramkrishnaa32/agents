

# imports
from openai import OpenAI
from logging import getLogger
logger = getLogger(__name__)

class openaiHelper:
    """Helper class to interact with the OpenAI API using the OpenAI Python client"""
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)


    def get_response(self, model="gpt-4o-mini", messages=[]):
        """Get a response from the OpenAI API"""
        return self.client.chat.completions.create(
            model=model,
            messages=messages
        )


    

