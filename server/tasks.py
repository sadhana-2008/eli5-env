from dataclasses import dataclass
from typing import List

@dataclass
class CodeTask:
    id: str
    difficulty: str
    description: str
    bad_code: str
    issues: List[str]
    max_score: float = 1.0

TASKS = {
    "easy": CodeTask(
        id="easy",
        difficulty="easy",
        description="Review this Python function for basic code quality issues.",
        bad_code="""
def f(x):
    l = []
    for i in range(len(x)):
        l.append(x[i] * 2)
    return l
""",
        issues=[
            "function name 'f' is not descriptive",
            "variable name 'l' is not descriptive",
            "should use list comprehension instead of for loop",
            "should use enumerate or direct iteration instead of range(len(x))",
        ]
    ),

    "medium": CodeTask(
        id="medium",
        difficulty="medium",
        description="Review this Python function for performance and design issues.",
        bad_code="""
def find_duplicates(items):
    duplicates = []
    for i in range(len(items)):
        for j in range(len(items)):
            if i != j and items[i] == items[j]:
                if items[i] not in duplicates:
                    duplicates.append(items[i])
    return duplicates
""",
        issues=[
            "O(n^2) time complexity, should use a set or dictionary",
            "checking 'not in duplicates' on a list is O(n), should use a set",
            "comparing every pair twice unnecessarily",
            "should use collections.Counter or set to find duplicates efficiently",
        ]
    ),

    "hard": CodeTask(
        id="hard",
        difficulty="hard",
        description="Review this Python function for security and subtle logic issues.",
        bad_code="""
import pickle
import os

def load_user_data(filename):
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            data = pickle.load(f)
            return data
    return {}

def save_user_data(data, filename):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)
""",
        issues=[
            "pickle.load is a critical security vulnerability - can execute arbitrary code",
            "filename is not sanitized - path traversal attack possible",
            "no error handling for corrupted pickle files",
            "should use json instead of pickle for user data",
            "no validation of the data structure after loading",
        ]
    ),
}