"""
Baseline inference script for Code Review Environment.
Runs a model against all 3 tasks and prints scores.

Usage:
    export OPENAI_API_KEY=your_key_here
    python inference.py
"""

import os
import requests
from openai import OpenAI

BASE_URL = os.environ.get("ENV_URL", "https://sadhana-srini-code-review-env.hf.space")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """You are an expert Python code reviewer. 
When given code, identify ALL issues including:
- Bad variable/function names
- Performance problems
- Security vulnerabilities  
- Poor coding practices
- Wrong data structures

Be specific and actionable in your review."""

def run_episode(task_id: str) -> float:
    """Run one full episode for a given task. Returns final score."""
    
    # reset environment
    reset_response = requests.post(
        f"{BASE_URL}/reset",
        json={"task_id": task_id}
    )
    data = reset_response.json()
    obs = data["observation"]
    
    print(f"\n--- Task: {task_id.upper()} ---")
    print(f"Code to review:\n{obs['code']}")
    
    done = False
    final_score = 0.0
    attempt = 0

    while not done:
        attempt += 1
        print(f"\nAttempt {attempt}...")

        # generate review using OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Review this code and identify all issues:\n\n{obs['code']}"}
            ],
            max_tokens=500
        )

        review = response.choices[0].message.content
        print(f"Review: {review[:200]}...")

        # submit review to environment
        step_response = requests.post(
            f"{BASE_URL}/step",
            json={"review": review, "task_id": task_id}
        )
        step_data = step_response.json()
        obs = step_data["observation"]
        done = step_data["done"]
        final_score = obs["score"]

        print(f"Score: {final_score:.2f} | Issues caught: {obs['issues_caught']}/{obs['total_issues']}")
        print(f"Feedback: {obs['feedback']}")

    return final_score


def main():
    print("=== Code Review Environment Baseline ===")
    print(f"Environment URL: {BASE_URL}")
    
    # check health
    health = requests.get(f"{BASE_URL}/health").json()
    print(f"Health: {health}")

    scores = {}
    for task_id in ["easy", "medium", "hard"]:
        score = run_episode(task_id)
        scores[task_id] = score

    print("\n=== FINAL SCORES ===")
    for task_id, score in scores.items():
        bar = "█" * int(score * 20)
        print(f"{task_id:10s} [{bar:<20}] {score:.2f}")
    
    avg = sum(scores.values()) / len(scores)
    print(f"\nAverage score: {avg:.2f}")


if __name__ == "__main__":
    main()