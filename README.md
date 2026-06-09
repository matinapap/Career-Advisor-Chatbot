# 🤖 Career Advisor Pipeline

An AI career guidance chatbot built for Google Colab. It analyzes a user profile, suggests career roles, generates learning paths, gives resume feedback with RAG, and creates mock interview practice.

The project is organized as a normal Python package with one lightweight Colab notebook for orchestration.

---

## ✨ Features

- **Open-source Greek-capable LLM by default**: `ilsp/Meltemi-7B-Instruct-v1`
- **Optional Gemini fallback** via `LLM_PROVIDER=gemini`
- **LangGraph pipelines** for career guidance workflows
- **Pydantic structured outputs** for role and skill parsing
- **RAG resume feedback** using FAISS and HuggingFace embeddings
- **SerpAPI course search** for personalized learning recommendations
- **Gradio UI** for an interactive demo
- **Unit tests** for core helpers and structured parsing

The default model is ILSP's Meltemi 7B Instruct, a Greek/English text-generation model published on Hugging Face with an Apache-2.0 license. For Colab, use a GPU runtime such as T4.

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

4. Use a GPU runtime:

```text
Runtime -> Change runtime type -> T4 GPU
```

5. Optional: add `SERPAPI_KEY` in Colab Secrets if you want live course search. Without it, the app still runs, but course search returns a missing-key message.

6. Run tests:

```python
!pytest -q
```

7. Launch the UI:

```python
from career_advisor.app import demo

demo.launch(share=True, debug=False)
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

The default Hugging Face model is large, so local usage works best on a machine with a suitable GPU. For CPU-only local runs, use a smaller `HF_MODEL_ID` or switch to `LLM_PROVIDER=gemini`.

Run tests:

```bash
pytest -q
```

Useful environment variables:

```text
LLM_PROVIDER=hf
HF_MODEL_ID=ilsp/Meltemi-7B-Instruct-v1
HF_USE_4BIT=true
HF_MAX_NEW_TOKENS=768
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
