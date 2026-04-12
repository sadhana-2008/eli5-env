---
title: Code Review Environment
emoji: 🏆
colorFrom: gray
colorTo: purple
sdk: docker
pinned: false
license: mit
short_description: Can an AI catch security bugs before they ship? Find out.
tags:
- openenv
---

# 🔍 Code Review Environment

An OpenEnv reinforcement learning environment where AI agents must review 
bad code and identify real issues — from sloppy variable names to critical 
security vulnerabilities.

## 🤔 Why This Exists

Code review is one of the most important tasks in software engineering. 
Every day, engineers miss bugs, security holes, and performance issues in 
code review. This environment trains AI agents to get better at it — 
systematically, measurably, and across difficulty levels.

## 🎮 How It Works

1. Environment gives the agent a piece of bad Python code
2. Agent writes a code review identifying issues
3. A **real LLM judge** (Llama 3.1) scores the review 0.0 → 1.0
4. Score ≥ 0.8 = success. Agent wins the episode.
5. Agent gets 3 attempts per task.

## 📊 Three Tasks — Easy to Hard

| Task | Difficulty | What to catch |
|------|-----------|---------------|
| `easy` | 🟢 Easy | Bad variable names, missing list comprehensions |
| `medium` | 🟡 Medium | O(n²) complexity, inefficient data structures |
| `hard` | 🔴 Hard | Security vulnerabilities, pickle attacks, path traversal |

## 🚀 Try It Live

```bash
# Reset — get a task
curl -X POST https://sadhana-srini-code-review-env.hf.space/reset \
  -H "Content-Type: application/json" \
  -d '{"task_id": "easy"}'

# Step — submit your review
curl -X POST https://sadhana-srini-code-review-env.hf.space/step \
  -H "Content-Type: application/json" \
  -d '{"review": "the function name f is not descriptive", "task_id": "easy"}'
```

Or try the interactive docs:
👉 https://sadhana-srini-code-review-env.hf.space/docs

## 🍫 Reward Signal

| Score | Meaning |
|-------|---------|
| 1.0 | Caught all issues |
| 0.8 | Caught most issues |
| 0.5 | Caught some issues |
| 0.0 | Missed everything |

Partial credit is given throughout the episode — not just at the end.

## 🛠️ Built With

- **OpenEnv** — Meta x HuggingFace RL environment framework
- **FastAPI** — environment server
- **Llama 3.1 8B** — LLM grader via HuggingFace Inference API
- **Docker** — containerized deployment

## 🏃 Run Baseline

```bash
export OPENAI_API_KEY=your_key
export ENV_URL=https://sadhana-srini-code-review-env.hf.space
python inference.py
```

## ⭐ Authors

**Sadhana Srinivasan** — SOAI @ Sai University  
**Vaibhav B** — SCDS @ Sai University  
**Sahana Mukundan** — SCDS @ Sai University
