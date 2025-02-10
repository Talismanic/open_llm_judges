import os
from pydantic_ai.models.gemini import GeminiModel as PydanticGeminiModel

class GeminiModel:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        self.model_name = 'gemini-2.0-flash'
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")

        self.model = PydanticGeminiModel( 'gemini-2.0-flash', api_key=self.api_key)

    def get_model(self):
        """
        Returns the OpenAI model instance.
        """
        return self.model
