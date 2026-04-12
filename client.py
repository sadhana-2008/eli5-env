import requests
from typing import Optional
from models import CodeReviewAction, CodeReviewObservation, CodeReviewState

class CodeReviewEnv:
    """Client to connect to the Code Review OpenEnv environment."""

    def __init__(self, base_url: str = "https://sadhana-srini-code-review-env.hf.space"):
        self.base_url = base_url.rstrip("/")

    def reset(self, task_id: str = "easy") -> CodeReviewObservation:
        response = requests.post(
            f"{self.base_url}/reset",
            json={"task_id": task_id}
        )
        data = response.json()
        obs = data["observation"]
        return CodeReviewObservation(**obs)

    def step(self, action: CodeReviewAction) -> dict:
        response = requests.post(
            f"{self.base_url}/step",
            json={
                "review": action.review,
                "task_id": action.task_id
            }
        )
        data = response.json()
        obs = data["observation"]
        return {
            "observation": CodeReviewObservation(**obs),
            "reward": data.get("reward"),
            "done": data.get("done")
        }

    def state(self) -> CodeReviewState:
        response = requests.get(f"{self.base_url}/state")
        return CodeReviewState(**response.json())

    def health(self) -> bool:
        try:
            response = requests.get(f"{self.base_url}/health")
            return response.json().get("status") == "ok"
        except:
            return False