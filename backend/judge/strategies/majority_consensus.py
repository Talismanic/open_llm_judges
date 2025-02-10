from typing import List
from pydantic_ai import Agent
from collections import Counter

class MajorityConsensusStrategy:
    def execute(self, workers: List[Agent], task_info: str) -> List[str]:
        """
        Executes (2n+1) worker agents and determines the majority consensus.
        """
        worker_results = []
        for agent in workers:
            try:
                result = agent.run_sync(task_info).data
                worker_results.append(result)
            except Exception as exc:
                worker_results.append(f"Error: {exc}")
        
        result_counts = Counter(worker_results)
        majority_result = result_counts.most_common(1)[0][0]
        print("Majority Consensus Decision:", majority_result)
        return majority_result
