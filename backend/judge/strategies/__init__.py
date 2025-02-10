from .majority_consensus import MajorityConsensusStrategy
from .multi_worker import MultiWorkerStrategy
from .single_worker import SingleWorkerStrategy
strategies = {
        1: SingleWorkerStrategy(),
        2: MultiWorkerStrategy(),
        3: MajorityConsensusStrategy()
    }