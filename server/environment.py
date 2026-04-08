import random
import uuid
import os
from huggingface_hub import InferenceClient

CONCEPTS = [
    "recursion", "gravity", "the internet",
    "DNA", "machine learning", "black holes",
    "democracy", "inflation", "photosynthesis",
    "electricity", "evolution", "climate change",
    "the stock market", "quantum computing", "vaccines"
]

HF_TOKEN = os.environ.get("HF_TOKEN", "")

class ELI5Environment:
    def __init__(self):
        self._concept = ""
        self._attempts = 0
        self._max_attempts = 3
        self._episode_id = None
        self._client = InferenceClient(
            provider="novita",
            api_key=HF_TOKEN,
        )

    def reset(self):
        self._concept = random.choice(CONCEPTS)
        self._attempts = 0
        self._episode_id = str(uuid.uuid4())
        return {
            "observation": {
                "concept": self._concept,
                "feedback": f"Explain '{self._concept}' like I'm 5 years old!",
                "score": 0.0,
                "attempts_remaining": self._max_attempts
            },
            "done": False,
            "reward": None
        }

    def step(self, action: dict):
        explanation = action.get("explanation", "")
        self._attempts += 1
        attempts_remaining = self._max_attempts - self._attempts

        score = self._grade(explanation, self._concept)
        done = score >= 0.8 or attempts_remaining <= 0

        if score >= 0.8:
            feedback = f"Great job! A 5 year old would understand that! Score: {score:.2f}"
        elif attempts_remaining <= 0:
            feedback = f"Out of attempts! The concept was '{self._concept}'. Score: {score:.2f}"
        else:
            feedback = f"Too complex! Try simpler words. Score: {score:.2f}. {attempts_remaining} attempts left."

        return {
            "observation": {
                "concept": self._concept,
                "feedback": feedback,
                "score": score,
                "attempts_remaining": attempts_remaining
            },
            "done": done,
            "reward": score if done else 0.0
        }

    def state(self):
        return {
            "episode_id": self._episode_id,
            "step_count": self._attempts,
            "concept": self._concept,
            "max_attempts": self._max_attempts
        }

    def _grade(self, explanation: str, concept: str) -> float:
        try:
            response = self._client.chat.completions.create(
                model="meta-llama/Llama-3.1-8B-Instruct",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a grader. You only respond with a single number between 0.0 and 1.0. Nothing else."
                    },
                    {
                        "role": "user",
                        "content": f"""Rate how well this explanation of '{concept}' would be understood by a 5 year old.
                        
Explanation: {explanation}

Rules:
- 1.0 = perfect, simple words, fun analogy, a child would totally get it
- 0.5 = okay but still a bit complex
- 0.0 = way too technical, no child would understand

Respond with only a number like 0.7"""
                    }
                ],
                max_tokens=5,
            )
            score_text = response.choices[0].message.content.strip()
            return min(max(float(score_text), 0.0), 1.0)
        except Exception as e:
            print(f"Grader error: {e}")
            return self._fallback_grade(explanation)

    def _fallback_grade(self, explanation: str) -> float:
        words = explanation.split()
        score = 0.0
        if 10 <= len(words) <= 50:
            score += 0.3
        complex_words = ["algorithm", "theoretical", "approximately",
                        "fundamental", "mechanism", "sophisticated"]
        complex_count = sum(1 for w in complex_words if w in explanation.lower())
        score += max(0, 0.3 - (complex_count * 0.1))
        analogy_words = ["like", "imagine", "think of", "similar to", "just like"]
        if any(w in explanation.lower() for w in analogy_words):
            score += 0.4
        return min(score, 1.0)