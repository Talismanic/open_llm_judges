from judge.agents.agent_utils import AgentUtils
from judge.strategies.majority_consensus import MajorityConsensusStrategy
from judge.strategies.multi_worker import MultiWorkerStrategy
from judge.strategies.single_worker import SingleWorkerStrategy


class LLMJudgeSystem:
    def __init__(self, archetype, num_agents, task_meta, task, worker_agent_models):
        self.strategy = None
        self.task_meta = task_meta  # Now a string, not JSON
        self.num_agents = num_agents
        self.worker_agent_models = worker_agent_models
        self.worker_agents = []
        self.judge_agent = None
        self.task = task
        self.worker_output = []
        self.archetype = archetype

        self.setup_strategy()
        self.setup_agents()

    def setup_strategy(self):
        """Set the execution strategy based on the archetype"""
        if self.archetype == 1:
            self.strategy = SingleWorkerStrategy()
        elif self.archetype == 2:
            self.strategy = MultiWorkerStrategy()
        elif self.archetype == 3:
            self.strategy = MajorityConsensusStrategy()
        else:
            raise ValueError("Invalid archetype selected")

    def setup_agents(self):
        """Configure worker and judge agents dynamically"""
        self.task_meta, self.worker_agents, self.judge_agent = AgentUtils.configure_agents(
            self.num_agents, self.task_meta, self.worker_agent_models
        )

    def run(self):
        """Execute the worker process and judge evaluation"""
        if not self.strategy:
            return {"error": "No valid strategy selected"}

        # Execute workers
        self.worker_output = self.strategy.execute(self.worker_agents, self.task)

        if int(self.archetype) == 1:
            # Single worker single judge mode
            judge_input = self.task + "\n" + self.worker_output
            judge_result = self.judge_agent.run_sync(judge_input)
            return {"worker_output": self.worker_output, "judge_decision": judge_result.data}

        elif int(self.archetype) == 2:
            # Combine worker outputs for the judge
            combined_worker_output = "\n".join(self.worker_output)
            judge_input = self.task + "\n" + combined_worker_output
            judge_result = self.judge_agent.run_sync(judge_input)
            return {"worker_output": combined_worker_output, "judge_decision": judge_result.data}
        else:
            # Majority consensus mode
            return {"consensus_decision": self.worker_output}
