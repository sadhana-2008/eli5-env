from typing import Optional
from openenv.core.env_server import Action, Observation, State

class ELI5Action(Action):
    explanation: str  # what the AI writes to explain the concept

class ELI5Observation(Observation):
    concept: str              # e.g. "recursion", "black holes"
    feedback: str             # e.g. "too complex, try simpler"
    score: float = 0.0        # 0.0 to 1.0
    attempts_remaining: int = 3

class ELI5State(State):
    concept: str = ""
    attempts: int = 0
    max_attempts: int = 3