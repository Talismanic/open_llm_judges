class JudgeAgent:
    def __init__(self, model, system_prompt: str):
        self.model = model
        self.system_prompt = system_prompt

    def run(self, input_text: str) -> str:
        """
        Use the judge model to evaluate the worker outputs combined with the task info.
        """
        response = self.model.run_sync(input_text, system_prompt=self.system_prompt)
        return response.data
