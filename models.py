from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class CodeReviewAction(BaseModel):
    """Action: AI submits a code review."""
    review: str
    task_id: str


class CodeReviewObservation(BaseModel):
    """Observation: what the AI sees."""
    task_id: str
    difficulty: str
    code: str
    description: str
    feedback: str = ""
    score: float = 0.0
    issues_caught: int = 0
    total_issues: int = 0
    attempts_remaining: int = 3
    done: bool = False
    reward: Optional[float] = None


class CodeReviewState(BaseModel):
    """Episode metadata."""
    episode_id: Optional[str] = None
    step_count: int = 0
    current_task: str = ""
    max_attempts: int = 3
    scores: Dict[str, float] = {}


class TaskResult(BaseModel):
    """Result of a single task attempt."""
    task_id: str
    score: float
    issues_caught: List[str] = []
    issues_missed: List[str] = []
    feedback: str = ""