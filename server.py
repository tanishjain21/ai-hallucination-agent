from fastapi import FastAPI
import random
import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data import dataset

app = FastAPI()

current_case = None
step_count = 0
max_steps = 3


def check_correctness(llm_response, correct_answer, context=""):
    llm = llm_response.lower().strip()
    correct = correct_answer.lower().strip()

    if correct == "not mentioned":
        if any(p in llm for p in [
            "not mentioned", "not provided", "not stated",
            "cannot determine", "not available", "no information"
        ]):
            return 1.0
        return 0.0

    if correct in ["no", "do not", "don't", "never"]:
        said_no = any(neg in llm for neg in [
            "no", "do not", "don't", "never",
            "contraindicated", "should not", "must not"
        ])
        if not said_no:
            return 0.0
        llm_numbers = re.findall(r'\d+\.?\d*', llm)
        context_numbers = re.findall(r'\d+\.?\d*', context)
        if any(n not in context_numbers for n in llm_numbers):
            return 0.0
        return 1.0

    correct_numbers = set(re.findall(r'\d+\.?\d*', correct))
    if correct_numbers:
        llm_numbers = set(re.findall(r'\d+\.?\d*', llm))
        if not correct_numbers.issubset(llm_numbers):
            return 0.3

    synonym_map = {
        "doctor": "physician",
        "epi": "epinephrine",
        "adrenaline": "epinephrine",
        "narcan": "naloxone",
        "heart attack": "myocardial infarction",
        "bp": "blood pressure",
        "cpr": "cardiopulmonary resuscitation"
    }
    for word, canonical in synonym_map.items():
        llm = llm.replace(word, canonical)
        correct = correct.replace(word, canonical)

    llm_tokens = set(re.findall(r'\w+', llm))
    correct_tokens = set(re.findall(r'\w+', correct))

    if not correct_tokens:
        return 0.0

    overlap = len(llm_tokens & correct_tokens) / len(correct_tokens)
    return overlap


@app.post("/reset")
def reset():
    global current_case, step_count
    current_case = random.choice(dataset)
    step_count = 0
    return {
        "query": current_case["query"],
        "context": current_case["context"],
        "difficulty": current_case.get("difficulty", "easy")
    }


@app.post("/step")
def step(action: str, llm_response: str):
    global step_count

    if current_case is None:
        return {"error": "Call /reset first"}

    step_count += 1

    score = check_correctness(
        llm_response,
        current_case["correct_answer"],
        current_case["context"]
    )

    if score >= 0.6:
        status = "correct"
    elif score >= 0.3:
        status = "partial"
    else:
        status = "wrong"

    if status == "correct" and action == "approve_response":
        reward = 1.0
    elif status == "correct" and action == "flag_hallucination":
        reward = -0.5
    elif status == "partial" and action == "approve_response":
        reward = 0.5
    elif status == "wrong" and action == "flag_hallucination":
        reward = 1.0
    elif status == "wrong" and action == "approve_response":
        reward = -1.0
    else:
        reward = -0.2

    reward = max(-1.0, min(1.0, reward))
    done = step_count >= max_steps or status == "correct"

    return {
        "reward": reward,
        "status": status,
        "difficulty": current_case.get("difficulty", "easy"),
        "correct_answer": current_case["correct_answer"],
        "steps_used": step_count,
        "done": done
    }


@app.get("/state")
def state():
    if current_case is None:
        return {
            "active": False,
            "step_count": step_count,
            "max_steps": max_steps,
            "current_case": None
        }
    return {
        "active": True,
        "step_count": step_count,
        "max_steps": max_steps,
        "current_case": {
            "query": current_case["query"],
            "context": current_case["context"],
            "difficulty": current_case.get("difficulty", "easy")
        }
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "active_case": current_case is not None,
        "step_count": step_count
    }


def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()