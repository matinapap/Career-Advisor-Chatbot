# 🤖 Career Advisor Pipeline

An AI career guidance chatbot built for Google Colab. It analyzes a user profile, suggests career roles, generates learning paths, gives resume feedback with RAG, and creates mock interview practice.

The project is organized as a normal Python package with one lightweight Colab notebook for orchestration.

---

## ✨ Features

- **Open-source Colab-friendly LLM by default**: `Qwen/Qwen2.5-0.5B-Instruct`
- **Optional Gemini fallback** via `LLM_PROVIDER=gemini`
- **LangGraph pipelines** for career guidance workflows
- **Pydantic structured outputs** for role and skill parsing
- **RAG resume feedback** using FAISS and HuggingFace embeddings
- **SerpAPI course search** for personalized learning recommendations
- **Gradio UI** for an interactive demo
- **Unit tests** for core helpers and structured parsing

The default model is a small open Hugging Face instruct model so the demo responds faster and is less likely to crash a free Colab runtime. For stronger output, you can override `HF_MODEL_ID=Qwen/Qwen2.5-1.5B-Instruct` or `HF_MODEL_ID=ilsp/Meltemi-7B-Instruct-v1` on a GPU runtime with enough memory.

---

## 📁 Project Structure

```text
notebooks/
  Career_Advisor.ipynb        # Single Colab orchestration notebook

career_advisor/
  __init__.py
  app.py                      # Gradio UI
  agents.py                   # Career advisor agent functions
  config.py                   # Paths, model settings, and secrets
  courses.py                  # SerpAPI course search
  llm.py                      # Hugging Face/Gemini LLM access and JSON parsing
  pdf.py                      # PDF text extraction
  pipeline.py                 # LangGraph pipeline orchestration
  preferences.py              # Local personalization preferences
  prompts.py                  # Prompt builders
  rag.py                      # Resume tips FAISS/RAG utilities
  schemas.py                  # Pydantic schemas for structured LLM output
  text_utils.py               # Output cleanup helpers

career_advisor_files/
  resume_tips.txt             # Local RAG knowledge base

tests/                        # Unit tests
requirements.txt              # Python dependencies
Presentation.pdf              # Project presentation
```

Runtime files such as `career_advisor_files/user_personalization.json` are intentionally ignored by git.

---

## 🧩 Architecture

The system has three LangGraph workflows:

- **Default Flow**: `Profile -> Role Suggestions -> Learning Path`
- **Personalized Flow**: `Profile -> Role Suggestions -> Personalized Learning`
- **Interview Flow**: `Profile -> Role Suggestions -> Resume Feedback -> Mock Interview`

Main components:

- `agents.py`: profile analysis, role suggestions, learning plans, resume advice, interviews
- `pipeline.py`: LangGraph nodes and graph execution
- `rag.py`: FAISS vector store over `resume_tips.txt`
- `llm.py`: model loading/generation and structured JSON validation
- `schemas.py`: Pydantic schemas for structured LLM responses
- `app.py`: Gradio interface

---

## 🚀 Running in Google Colab

1. Open `notebooks/Career_Advisor.ipynb`.
2. If needed, clone the repository:

```python
!git clone https://github.com/YOUR_USERNAME/Career-Advisor-Chatbot.git
%cd Career-Advisor-Chatbot
```

Replace `YOUR_USERNAME` with the GitHub account that hosts the repo.

3. Install dependencies:

```python
!pip install -r requirements.txt
```

4. Set the project root on the Python path:

```python
import os
import sys
from pathlib import Path

def find_project_root():
    candidates = [Path.cwd(), *Path.cwd().parents, Path("/content/Career-Advisor-Chatbot")]
    for candidate in candidates:
        if (candidate / "career_advisor").is_dir() and (candidate / "requirements.txt").is_file():
            return candidate
    raise RuntimeError("Run the clone/%cd cell first.")

PROJECT_ROOT = find_project_root()
os.chdir(PROJECT_ROOT)
os.environ["PYTHONPATH"] = str(PROJECT_ROOT)
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
```

5. Use a GPU runtime:

```text
Runtime -> Change runtime type -> T4 GPU
```

6. Optional: choose a model before launching:

```python
# Colab-safe default. Recommended for the demo.
%env HF_MODEL_ID=Qwen/Qwen2.5-0.5B-Instruct
%env HF_MAX_NEW_TOKENS=256
%env HF_INPUT_MAX_TOKENS=2048

# Better quality, slower.
# %env HF_MODEL_ID=Qwen/Qwen2.5-1.5B-Instruct
# %env HF_MAX_NEW_TOKENS=384

# Higher-quality Greek option, but much heavier and may crash small Colab runtimes.
# %env HF_MODEL_ID=ilsp/Meltemi-7B-Instruct-v1
# %env HF_MAX_NEW_TOKENS=768
```

7. Optional: add `SERPAPI_KEY` in Colab Secrets if you want live course search. Without it, the app still runs, but course search returns a missing-key message.

8. Run tests:

```python
!PYTHONPATH=$PWD pytest -q
```

9. Launch the UI:

```python
import os
import sys
from pathlib import Path

def find_project_root():
    candidates = [Path.cwd(), *Path.cwd().parents, Path("/content/Career-Advisor-Chatbot")]
    for candidate in candidates:
        if (candidate / "career_advisor").is_dir() and (candidate / "requirements.txt").is_file():
            return candidate
    raise RuntimeError("Run the clone/%cd cell first.")

PROJECT_ROOT = find_project_root()
os.chdir(PROJECT_ROOT)
os.environ["PYTHONPATH"] = str(PROJECT_ROOT)
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from career_advisor.app import demo

demo.launch(share=True, debug=True, show_error=True)
```

---

## 💻 Local Usage

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Gradio app:

```bash
python -m career_advisor.app
```

The default Hugging Face model is intentionally small enough for demos. For higher-quality output, use `HF_MODEL_ID=Qwen/Qwen2.5-1.5B-Instruct` or `HF_MODEL_ID=ilsp/Meltemi-7B-Instruct-v1` on a machine with a suitable GPU, or switch to `LLM_PROVIDER=gemini`.

Run tests:

```bash
pytest -q
```

Useful environment variables:

```text
LLM_PROVIDER=hf
HF_MODEL_ID=Qwen/Qwen2.5-0.5B-Instruct
HF_USE_4BIT=true
HF_MAX_NEW_TOKENS=256
HF_INPUT_MAX_TOKENS=2048
HF_TEMPERATURE=0.2
HF_TOP_P=0.9
SERPAPI_KEY=
```

To use Gemini instead of the default Hugging Face model:

```text
LLM_PROVIDER=gemini
GEMINI_API_KEY=...
GEMINI_MODEL_NAME=gemini-flash-latest
```

---

## 🧠 Pipeline Agents

### 🔍 Profile Analyzer

Processes a text-based profile and optional resume content. It extracts skills, knowledge, experience, and interests.

### 💼 Career Suggestion Agent

Produces career role recommendations with:

- justification
- required skills
- next steps

Role suggestions use Pydantic-validated structured JSON instead of regex parsing.

### 🎓 Learning Path Generator

Creates a learning plan for the selected role, including:

- technologies and concepts
- modules
- estimated duration
- course recommendations
- progression roadmap

### 📄 Resume Advisor

Uses RAG over `career_advisor_files/resume_tips.txt` to provide targeted resume feedback.

### 🗣️ Mock Interview Agent

Generates role-specific mock interview questions, model answers, and improvement tips.

### 🧭 Personalized Learning Agent

Uses `learning_style` and `career_goals` to build a personalized learning plan, extract skill gaps, and search for online courses.

---

## 📊 Presentation

A visual overview is available here:

- [Career Advisor Pipeline Presentation](./Presentation.pdf)
