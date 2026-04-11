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

    # Handle "not mentioned" cases
    if correct == "not mentioned":
        not_mentioned_phrases = [
            "not mentioned", "not provided", "not stated",
            "cannot determine", "not available", "no information",
            "not specified", "unclear", "not given", "not indicated"
        ]
        if any(p in llm for p in not_mentioned_phrases):
            return 0.95
        llm_numbers = re.findall(r'\d+\.?\d*', llm)
        context_numbers = re.findall(r'\d+\.?\d*', context)
        if llm_numbers and not all(n in context_numbers for n in llm_numbers):
            return 0.05
        return 0.15

    # Handle negation cases
    if correct in ["no", "do not", "don't", "never"]:
        neg_phrases = [
            "no", "do not", "don't", "never",
            "contraindicated", "should not", "must not",
            "not recommended", "avoid", "not safe"
        ]
        said_no = any(neg in llm for neg in neg_phrases)
        if not said_no:
            return 0.05
        llm_numbers = re.findall(r'\d+\.?\d*', llm)
        context_numbers = re.findall(r'\d+\.?\d*', context)
        if any(n not in context_numbers for n in llm_numbers):
            return 0.05
        return 0.95

    # Number matching
    correct_numbers = set(re.findall(r'\d+\.?\d*', correct))
    llm_numbers = set(re.findall(r'\d+\.?\d*', llm))
    number_score = 0.0
    if correct_numbers:
        matched = correct_numbers.issubset(llm_numbers)
        number_score = 0.5 if matched else 0.1

    # Synonym normalization
    synonym_map = {
        "doctor": "physician",
        "epi": "epinephrine",
        "adrenaline": "epinephrine",
        "narcan": "naloxone",
        "heart attack": "myocardial infarction",
        "bp": "blood pressure",
        "cpr": "cardiopulmonary resuscitation",
        "o2": "oxygen",
        "hr": "heart rate",
        "temp": "temperature"
    }
    for word, canonical in synonym_map.items():
        llm = llm.replace(word, canonical)
        correct = correct.replace(word, canonical)

    # Token overlap score
    llm_tokens = set(re.findall(r'\w+', llm))
    correct_tokens = set(re.findall(r'\w+', correct))
    if not correct_tokens:
        return 0.05
    overlap = len(llm_tokens & correct_tokens) / len(correct_tokens)

    # Context faithfulness check
    context_tokens = set(re.findall(r'\w+', context.lower()))
    llm_token_list = re.findall(r'\w+', llm)
    hallucinated = [t for t in llm_token_list
                    if t not in context_tokens
                    and len(t) > 4
                    and t not in correct_tokens]
    hallucination_penalty = min(len(hallucinated) * 0.02, 0.3)

    # Combined score
    if correct_numbers:
        final_score = (number_score * 0.4) + (overlap * 0.6)
    else:
        final_score = overlap

    final_score = max(0.05, final_score - hallucination_penalty)
    return min(0.95, final_score)


@app.post("/reset")
def reset(seed: int = None):
    global current_case, step_count
    if seed is not None:
        random.seed(seed)
    current_case = random.choice(dataset)
    step_count = 0
    return {
        "query": current_case["query"],
        "context": current_case["context"],
        "difficulty": current_case.get("difficulty", "easy"),
        "seed": seed
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

    if action == "approve_response":
        if status == "correct":
            reward = 0.9
        elif status == "partial":
            reward = 0.5
        else:
            reward = -0.9
    elif action == "flag_hallucination":
        if status == "wrong":
            reward = 0.9
        elif status == "correct":
            reward = -0.4
        else:
            reward = 0.3
    elif action == "flag_incomplete":
        if status == "partial":
            reward = 0.8
        elif status == "wrong":
            reward = 0.5
        else:
            reward = -0.3
    else:
        reward = -0.2

    reward = max(-0.99, min(0.99, reward))
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