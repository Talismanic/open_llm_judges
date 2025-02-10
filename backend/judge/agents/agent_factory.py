import os
from pydantic_ai import Agent
from judge.models.openai_models import OpenAIModel
from judge.models.gemini_model import GeminiModel
# from pydantic_ai.models.gemini import GeminiModel
from openai import AsyncOpenAI

class AgentFactory:
    """
    Factory class for creating worker and judge agents.
    """

    @staticmethod
    def create_worker_agent(model_name: str, base_url: str, system_prompt: str, api_key: str = None) -> Agent:
        """
        Create a worker agent using an OpenAI-like model.
        """
        model = OpenAIModel(model_name=model_name, base_url=base_url, api_key=api_key).get_model()

        return Agent(model, system_prompt=system_prompt)

    @staticmethod
    def create_judge_agent(system_prompt: str) -> Agent:
        """
        Create a judge agent using the Gemini model.
        The GEMINI_API_KEY is obtained from the OS environment.
        """
        model = GeminiModel().get_model()
        return Agent(model, system_prompt=system_prompt)
