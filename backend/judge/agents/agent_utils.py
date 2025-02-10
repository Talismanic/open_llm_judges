from .agent_factory import AgentFactory
from judge.prompts.system_prompts import SystemPromptGeneratorAgent

class AgentUtils:
    @staticmethod
    def configure_agents(num_agents, task_meta, worker_agent_models):
        """
        Configures worker and judge agents dynamically.
        
        - Uses `task_meta` to generate system prompts.
        - Uses `worker_agent_models` to create worker agents dynamically.
        - Creates a judge agent using `AgentFactory`.
        """

        # Generate system prompts from the string task_meta
        prompt_generator = SystemPromptGeneratorAgent()
        prompts = prompt_generator.generate_prompts(task_meta)

        worker_system_prompt = prompts.get("worker_prompt", "Default worker prompt")
        judge_system_prompt = prompts.get("judge_prompt", "Default judge prompt")

        # Create Worker Agents
        worker_agents = []
        for agent_data in worker_agent_models:
            model_name = agent_data["model_name"]
            base_url = agent_data["endpoint"] or 'http://localhost:11434/v1' # Renamed for clarity
            api_key = agent_data.get("api_key", None)

            worker_agents.append(
                AgentFactory.create_worker_agent(model_name, base_url, worker_system_prompt, api_key)
            )

        # Create Judge Agent
        judge_agent = AgentFactory.create_judge_agent(judge_system_prompt)

        return task_meta, worker_agents, judge_agent
