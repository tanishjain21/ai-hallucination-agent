# 🧠 AI Hallucination Detection & Correction Agent

An intelligent reinforcement learning environment where an AI agent learns to 
detect and correct hallucinations in LLM responses for critical medical Q&A scenarios.

## 🎯 Problem Statement

Large Language Models (LLMs) frequently hallucinate — generating confident but 
factually incorrect medical information. In healthcare contexts, this is dangerous 
and can lead to patient harm. This project addresses this critical problem by 
building an RL environment where an agent:

1. **Detects** when an LLM response contains hallucinated information
2. **Classifies** whether the response is wrong or just incomplete
3. **Corrects** hallucinated responses using only verified context
4. **Learns** optimal detection strategies through reward-based feedback

## 🏗️ Architecture
┌─────────────────────────────────────────────────────┐
│                   inference.py (Agent)               │
│                                                      │
│  ┌──────────┐   ┌──────────┐   ┌──────────────────┐ │
│  │Generator │──▶│ Detector │──▶│    Corrector     │ │
│  │          │   │          │   │                  │ │
│  │LLM Query │   │Hallucin- │   │Fix using context │ │
│  │Response  │   │ation Check   │only              │ │
│  └──────────┘   └──────────┘   └──────────────────┘ │
└─────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────┐
│                   server.py (Environment)            │
│                                                      │
│  /reset  →  Load random medical case                 │
│  /step   →  Evaluate action, return reward           │
│  /state  →  Get current environment state            │
│  /health →  Health check                             │
└─────────────────────────────────────────────────────┘

## 🔄 Agent Pipeline

reset() → get medical query + context
LLM generates response
Agent judges response:

APPROVE → fully supported by context
FLAG_HALLUCINATION → adds info not in context
FLAG_INCOMPLETE → missing key information


If hallucination detected:

Auto-correct using context only
Re-judge corrected response


Submit final action to environment
Receive reward signal
Repeat for MAX_STEPS


## 🎮 Action Space

| Action | Description | When to Use |
|--------|-------------|-------------|
| `approve_response` | Response is grounded in context | Answer matches context exactly |
| `flag_hallucination` | Response adds fabricated information | Answer contains info not in context |
| `flag_incomplete` | Response is missing key information | Answer is partially correct |

## 🏆 Reward Structure

| Status | Action | Reward |
|--------|--------|--------|
| Correct | approve_response | +0.9 |
| Wrong | flag_hallucination | +0.9 |
| Partial | flag_incomplete | +0.8 |
| Partial | approve_response | +0.5 |
| Wrong | flag_incomplete | +0.5 |
| Correct | flag_hallucination | -0.4 |
| Correct | flag_incomplete | -0.3 |
| Wrong | approve_response | -0.9 |

## 📊 Dataset

40 medical Q&A cases across 3 difficulty levels:

### 🟢 Easy (10 cases)
- Direct retrieval from clear context
- Single fact answers
- Examples: drug dosages, procedures, positions

### 🟡 Medium (10 cases)
- Synonym resolution required
- Negation handling
- Partial inference needed
- Examples: drug name aliases, contraindications

### 🔴 Hard (20 cases)
- Missing information traps
- Adversarial contexts
- Forced hallucination scenarios
- Examples: incomplete patient data, dangerous drug interactions

## 🧪 Grader Design

The grader uses multiple strategies for accurate scoring:

1. **Not-mentioned detection** — checks if LLM correctly identifies missing info
2. **Negation handling** — validates correct negative responses
3. **Number matching** — ensures dosages and values are accurate
4. **Synonym normalization** — handles medical term aliases
5. **Token overlap scoring** — measures semantic similarity
6. **Hallucination penalty** — penalizes words not grounded in context
7. **Combined scoring** — weighted combination of all signals

## 🚀 Setup

### Environment Variables
```bash
API_BASE_URL=<your-api-endpoint>
API_KEY=<your-api-key>
MODEL_NAME=llama-3.3-70b-versatile
HF_TOKEN=<your-hf-token>
```

### Run Locally
```bash
pip install -r requirements.txt
uvicorn server:app --host 0.0.0.0 --port 7860 &
sleep 5
python inference.py
```

### Docker
```bash
docker build -t hallucination-agent .
docker run -p 7860:7860 \
  -e API_BASE_URL=<url> \
  -e API_KEY=<key> \
  -e MODEL_NAME=llama-3.3-70b-versatile \
  hallucination-agent
```

## 📈 Scoring

- Each step reward normalized to `(0, 1)`
- Episode score = average of normalized rewards
- Final score clamped to `(0.01, 0.99)`
- Success threshold = 0.5
- 5 episodes per evaluation run

## 🏥 Medical Safety Focus

This environment prioritizes patient safety by:
- Never approving responses with fabricated dosages or procedures
- Flagging responses that add information not verified in context
- Automatically correcting hallucinations before final submission
- Handling edge cases like missing information gracefully
- Penalizing overconfident wrong answers heavily (-0.9)

## 🔬 Real-world Applications

This environment can be used to:
- **Train** LLM agents to be more careful with medical information
- **Evaluate** how well models stay grounded in provided context
- **Benchmark** hallucination detection across difficulty levels
- **Research** correction mechanisms for medical AI systems

## 📁 Project Structure
ai-hallucination-agent/
├── server.py          # FastAPI environment server
├── inference.py       # Baseline agent script
├── data.py            # 40 medical Q&A cases
├── openenv.yaml       # OpenEnv configuration
├── Dockerfile         # Docker configuration
├── requirements.txt   # Python dependencies
└── README.md          # This file

## 🤝 OpenEnv Compliance

- ✅ `/reset` endpoint returns clean initial state
- ✅ `/step` endpoint accepts action and returns reward
- ✅ `/state` endpoint returns current environment state
- ✅ `/health` endpoint for liveness check
- ✅ Structured stdout logs `[START]` `[STEP]` `[END]`
- ✅ Score strictly between `(0, 1)`
- ✅ Docker builds and runs successfully
- ✅ HuggingFace Space deploys and responds
