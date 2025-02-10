import os
import json
import re
import asyncio
from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel

class SystemPromptGeneratorAgent:
    def __init__(self):
        """
        Initializes the System Prompt Generator Agent using the Gemini model.
        """
        gemini_api_key = os.environ.get("GEMINI_API_KEY")
        if not gemini_api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        
        self.model = GeminiModel('gemini-2.0-flash', api_key=gemini_api_key)

    def generate_prompts(self, task_description: str) -> dict:
        """
        Generates system prompts for the Worker Agent and Judge Agent.
        """
        prompt_template = f"""
        Given the following task description, generate:
        - A system prompt for a worker agent that explains its role in solving the task.
        - A system prompt for a judge agent that explains its role in evaluating the worker's outputs.

        Task Description: {task_description}

        Expected Output Format (strict JSON with double quotes):
        {{
            "worker_prompt": "<Instructions for the worker agent>",
            "judge_prompt": "<Instructions for the judge agent>"
        }}
        """
        
        gemini_prompt_generator_agent = Agent(self.model, system_prompt='You are a prompt generator agent')

        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        future = asyncio.ensure_future(gemini_prompt_generator_agent.run(prompt_template))
        gemini_prompt_generator_agent_result = loop.run_until_complete(future)

        response = gemini_prompt_generator_agent_result.data
        cleaned_response = re.sub(r"^```(?:json)?\n|\n```$", "", response.strip())

        try:
            return json.loads(cleaned_response)  # Convert string to dictionary
        except json.JSONDecodeError:
            raise ValueError(f"Failed to parse response as JSON after cleaning: {cleaned_response}")
