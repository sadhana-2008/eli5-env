from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.environment import CodeReviewEnvironment

app = FastAPI(
    title="Code Review Environment",
    description="An OpenEnv RL environment where AI agents review bad code and identify issues.",
    version="1.0.0"
)

env = CodeReviewEnvironment()

class ResetRequest(BaseModel):
    task_id: Optional[str] = "easy"

class StepRequest(BaseModel):
    review: str
    task_id: Optional[str] = "easy"

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/reset")
def reset(request: ResetRequest):
    return env.reset(task_id=request.task_id)

@app.post("/step")
def step(request: StepRequest):
    return env.step({"review": request.review, "task_id": request.task_id})

@app.get("/state")
def state():
    return env.state()

@app.get("/tasks")
def get_tasks():
    from server.tasks import TASKS
    return {
        task_id: {
            "difficulty": task.difficulty,
            "description": task.description,
            "total_issues": len(task.issues)
        }
        for task_id, task in TASKS.items()
    }