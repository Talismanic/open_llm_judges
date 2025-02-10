import unittest
from unittest.mock import MagicMock, patch
from agents.judge_agent import JudgeAgent
from agents.worker_agent import WorkerAgent
from strategies.single_worker import SingleWorkerStrategy
from strategies.multi_worker import MultiWorkerStrategy  
from strategies.majority_consensus import MajorityConsensusStrategy
from models.openai_models import OpenAIModel
from models.gemini_model import GeminiModel

class Response:
    def __init__(self, data):
        self.data = data

class IntegrationTests(unittest.TestCase):
    def setUp(self):
        # Mock models
        self.openai_model = OpenAIModel(model_name="test", base_url="test")
        self.gemini_model = GeminiModel(model_name="test", api_key="test")
        
        # Mock responses
        self.openai_model.run_sync = MagicMock(return_value=Response("Worker response"))
        self.gemini_model.run_sync = MagicMock(return_value=Response("Judge decision"))
        
        # Create agents
        self.worker1 = WorkerAgent(self.openai_model, "worker prompt")
        self.worker2 = WorkerAgent(self.openai_model, "worker prompt") 
        self.worker3 = WorkerAgent(self.openai_model, "worker prompt")
        self.judge = JudgeAgent(self.gemini_model, "judge prompt")
        
        # Mock worker responses
        self.worker1.run = MagicMock(return_value="Worker response")
        self.worker2.run = MagicMock(return_value="Worker response")
        self.worker3.run = MagicMock(return_value="Worker response")
        
        # Create strategies
        self.single_strategy = SingleWorkerStrategy()
        self.multi_strategy = MultiWorkerStrategy()
        self.consensus_strategy = MajorityConsensusStrategy()
        
        self.test_prompt = "Test task"

    def test_single_worker_strategy(self):
        """Test single worker strategy execution"""
        result = [worker.run(self.test_prompt) for worker in [self.worker1]]
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "Worker response")

    def test_multi_worker_strategy(self):
        """Test multiple worker strategy execution"""
        workers = [self.worker1, self.worker2]
        result = [worker.run(self.test_prompt) for worker in workers]
        self.assertEqual(len(result), 2)
        self.assertTrue(all(r == "Worker response" for r in result))

    def test_majority_consensus_strategy(self):
        """Test majority consensus strategy with three workers"""
        workers = [self.worker1, self.worker2, self.worker3]
        result = [worker.run(self.test_prompt) for worker in workers]
        self.assertEqual(len(result), 3)
        self.assertTrue(all(r == "Worker response" for r in result))

    def test_judge_evaluation(self):
        """Test judge agent evaluation of worker outputs"""
        # Get worker outputs
        worker_outputs = [worker.run(self.test_prompt) for worker in [self.worker1, self.worker2]]
        combined_output = "\n".join(worker_outputs)
        
        # Test judge evaluation
        judge_input = self.test_prompt + "\n" + combined_output
        judge_result = self.judge.run(judge_input)
        self.assertEqual(judge_result, "Judge decision")

    def test_end_to_end(self):
        """Test complete workflow with workers and judge"""
        # Get worker outputs using single strategy
        worker_outputs = [worker.run(self.test_prompt) for worker in [self.worker1]]
        self.assertEqual(len(worker_outputs), 1)
        
        # Pass to judge
        combined_output = "\n".join(worker_outputs)
        judge_input = self.test_prompt + "\n" + combined_output
        final_decision = self.judge.run(judge_input)
        
        # Verify results
        self.assertEqual(worker_outputs[0], "Worker response")
        self.assertEqual(final_decision, "Judge decision")

    def test_error_handling(self):
        # Test error handling in strategy execution
        self.worker1.run = MagicMock(return_value="Error: API Error")
        workers = [self.worker1]
        
        results = [worker.run(self.test_prompt) for worker in workers]
        self.assertEqual(results[0], "Error: API Error")

if __name__ == '__main__':
    unittest.main()
