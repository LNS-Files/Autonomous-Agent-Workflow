# Autonomous Self-Correcting Multi-Agent Workflow

An AI Research Assistant that uses a **two-agent loop** — a Researcher and a Verifier — to produce accurate, self-checked answers. If the Verifier's score is too low, the system automatically retries until accuracy meets the target. Runs entirely **locally** with [Ollama](https://ollama.com/) — no cloud API required.

---

## How It Works

```
User Question
      │
      ▼
┌─────────────┐
│  Researcher  │  ← looks up topic data, generates answer
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Verifier   │  ← critiques the answer, assigns SCORE 0.0–1.0
└──────┬──────┘
       │
   score < 0.8?
   ┌────┴────┐
  Yes        No
   │          │
   └──────────┤
  (retry)     ▼
           Final Answer shown to user
```

The graph is built with **LangGraph** and the loop continues until the verification score reaches 0.8 (configurable in `src/graph.py`).

---

## Features

- **Self-correcting loop** — automatically retries if accuracy is below the threshold
- **Dual-agent design** — separate Researcher and Verifier agents with distinct prompts
- **12 built-in research topics** — AI, Quantum Computing, Climate, Healthcare, Space, Crypto, Cybersecurity, Robotics, Energy, Education, Economics, Biotech
- **Streamlit UI** — accuracy target slider, per-round verification details, progress bar
- **100% local** — powered by Ollama (`llama3.2`), no internet or paid API needed

---

## Tech Stack

| Layer | Technology |
|---|---|
| UI | [Streamlit](https://streamlit.io/) |
| Agent orchestration | [LangGraph](https://github.com/langchain-ai/langgraph) |
| LLM framework | [LangChain](https://www.langchain.com/) |
| Local LLM | [Ollama](https://ollama.com/) — `llama3.2` |

---

## Project Structure

```
Autonomous-Agent-Workflow/
├── app.py           # Streamlit entry point
├── src/
│   ├── agents.py    # Researcher and Verifier node logic
│   ├── graph.py     # LangGraph workflow definition
│   ├── state.py     # Shared AgentState TypedDict
│   └── tools.py     # research_lookup tool (12 topic knowledge base)
├── .env             # Environment variables (not committed)
└── README.md
```

---

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) installed and running locally

Pull the model before running:

```bash
ollama pull llama3.2
```

---

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/LNS-Files/Autonomous-Agent-Workflow.git
cd Autonomous-Agent-Workflow

# 2. Create and activate a virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## Usage

1. Type a research question in the text box
2. Optionally adjust the **minimum accuracy target** slider in the sidebar
3. Click **Ask**
4. The system researches, verifies, and retries if needed
5. View the final answer and expand **"See how the answer was checked"** for per-round verification details

**Best results** come from questions that mention one of the supported topic keywords:
`AI` · `quantum` · `climate` · `health` · `space` · `crypto` · `cyber` · `robot` · `energy` · `education` · `economy` · `biotech`

---

## Configuration

| File | What to change |
|---|---|
| `src/graph.py` | Accuracy threshold (default `0.8`) |
| `src/agents.py` | Ollama model name (default `llama3.2`) |
| `src/tools.py` | Add or edit topic knowledge entries |

---

## License

MIT
