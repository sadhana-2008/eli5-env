import uuid
import os
from huggingface_hub import InferenceClient
from server.tasks import TASKS

HF_TOKEN = os.environ.get("HF_TOKEN", "")

client = InferenceClient(
    provider="novita",
    api_key=HF_TOKEN,
)

class CodeReviewEnvironment:
    def __init__(self):
        self._task_id = "easy"
        self._attempts = 0
        self._max_attempts = 3
        self._episode_id = None
        self._scores = {}

    def reset(self, task_id: str = "easy"):
        task = TASKS.get(task_id, TASKS["easy"])
        self._task_id = task_id
        self._attempts = 0
        self._episode_id = str(uuid.uuid4())
        self._scores = {}
        return {
            "observation": {
                "task_id": task_id,
                "difficulty": task.difficulty,
                "code": task.bad_code,
                "description": task.description,
                "feedback": "Review the code and identify all issues!",
                "score": 0.0,
                "issues_caught": 0,
                "total_issues": len(task.issues),
                "attempts_remaining": self._max_attempts,
                "done": False,
                "reward": None
            },
            "done": False,
            "reward": None,
            "info": {
                "task_id": task_id,
                "difficulty": task.difficulty,
                "total_issues": len(task.issues)
            }
        }

    def step(self, action: dict):
        review = action.get("review", "")
        task_id = action.get("task_id", self._task_id)
        task = TASKS.get(task_id, TASKS["easy"])
        self._attempts += 1
        attempts_remaining = self._max_attempts - self._attempts

        score, issues_caught, issues_missed = self._grade(review, task)
        self._scores[task_id] = score

        done = score >= 0.8 or attempts_remaining <= 0

        if score >= 0.8:
            feedback = f"Excellent review! Caught {len(issues_caught)}/{len(task.issues)} issues. Score: {score:.2f}"
        elif attempts_remaining <= 0:
            feedback = f"Out of attempts! Missed: {', '.join(issues_missed[:2])}. Score: {score:.2f}"
        else:
            feedback = f"Missed some issues: {', '.join(issues_missed[:2])}. Score: {score:.2f}. {attempts_remaining} attempts left."

        return {
            "observation": {
                "task_id": task_id,
                "difficulty": task.difficulty,
                "code": task.bad_code,
                "description": task.description,
                "feedback": feedback,
                "score": score,
                "issues_caught": len(issues_caught),
                "total_issues": len(task.issues),
                "attempts_remaining": attempts_remaining,
                "done": done,
                "reward": score if done else score * 0.5
            },
            "done": done,
            "reward": score if done else score * 0.5,
            "info": {
                "task_id": task_id,
                "difficulty": task.difficulty,
                "issues_caught": len(issues_caught),
                "issues_missed": len(issues_missed),
                "attempt": self._attempts
            }
        }

    def state(self):
        return {
            "episode_id": self._episode_id,
            "step_count": self._attempts,
            "current_task": self._task_id,
            "max_attempts": self._max_attempts,
            "scores": self._scores
        }

    def _grade(self, review: str, task):
        try:
            issues_list = "\n".join(f"- {issue}" for issue in task.issues)
            response = client.chat.completions.create(
                model="meta-llama/Llama-3.1-8B-Instruct",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a grader. Respond only in this exact format:\nSCORE: 0.0\nCAUGHT: issue1 | issue2\nMISSED: issue3 | issue4"
                    },
                    {
                        "role": "user",
                        "content": f"""Grade this code review.

Known issues in the code:
{issues_list}

Student review:
{review}

For each known issue, check if the review mentions it.
Respond in this exact format:
SCORE: [0.0-1.0 based on fraction of issues caught]
CAUGHT: [issues mentioned, separated by |]
MISSED: [issues not mentioned, separated by |]"""
                    }
                ],
                max_tokens=200,
                temperature=0,
            )
            return self._parse_grade(response.choices[0].message.content, task)
        except Exception as e:
            print(f"Grader error: {e}")
            return self._fallback_grade(review, task)

    def _parse_grade(self, response: str, task):
        lines = response.strip().split("\n")
        score = 0.0
        caught = []
        missed = []

        for line in lines:
            if line.startswith("SCORE:"):
                try:
                    score = float(line.replace("SCORE:", "").strip())
                except:
                    score = 0.0
            elif line.startswith("CAUGHT:"):
                caught = [x.strip() for x in line.replace("CAUGHT:", "").split("|") if x.strip()]
            elif line.startswith("MISSED:"):
                missed = [x.strip() for x in line.replace("MISSED:", "").split("|") if x.strip()]

        if not caught and not missed:
            missed = task.issues

        return min(max(score, 0.0), 1.0), caught, missed

    def _fallback_grade(self, review: str, task):
        review_lower = review.lower()
        caught = []
        missed = []
        for issue in task.issues:
            keywords = issue.lower().split()[:3]
            if any(kw in review_lower for kw in keywords):
                caught.append(issue)
            else:
                missed.append(issue)
        score = len(caught) / len(task.issues)
        return score, caught, missed
