from typing import List
from pydantic_ai import Agent

class MultiWorkerStrategy:
    def execute(self, workers: List[Agent], task_info: str) -> List[str]:
        """
        Executes multiple worker agents sequentially and returns their outputs.
        """
        results = []
        for agent in workers:
            try:
                result = agent.run_sync(task_info).data
                results.append(result)
            except Exception as exc:
                results.append(f"Error: {exc}")
        return results
