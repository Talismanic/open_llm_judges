from pydantic_ai.models.openai import OpenAIModel as PydanticOpenAIModel
from openai import AsyncOpenAI

class OpenAIModel:
    """
    Wrapper around Pydantic AI's OpenAI model for use in the agent factory.
    """

    def __init__(self, model_name: str, base_url: str, api_key: str = None):
        """
        Initializes the OpenAIModel instance.
        """
        client = AsyncOpenAI(
            base_url=base_url,
            api_key=api_key
            )
        self.model = PydanticOpenAIModel(
            model_name=model_name,
            openai_client=client
            )

    def get_model(self):
        """
        Returns the OpenAI model instance.
        """
        return self.model

