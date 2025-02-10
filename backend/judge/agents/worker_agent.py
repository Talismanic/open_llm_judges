class WorkerAgent:
    def __init__(self, model, system_prompt: str):
        self.model = model
        self.system_prompt = system_prompt

    def run(self, task_info: str) -> str:
        """
        Process the task_info with the assigned system prompt.
        In a real implementation this would call the model API.
        """
        response = self.model.run_sync(task_info, system_prompt=self.system_prompt)
        return response.data
