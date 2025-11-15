# 🤖 Career Advisor Pipeline — Google Colab + Gemini + LangGraph

Detailed description for the accompanying notebook / script.

---

## ✨ Overview
This project implements a complete career guidance system running on Google Colab, leveraging:

- **Gemini (google.generativeai)**
- **LangGraph and modular agents**
- **RAG using FAISS + HuggingFace embeddings**
- **SerpAPI for course search**
- **Gradio GUI**

The system analyzes user profiles, recommends suitable roles, generates learning plans, provides resume feedback (powered by RAG), and conducts mock interviews.

---

## 🧠 Pipeline Agents / Nodes

### 🔍 Profile Analyzer
- Processes the text-based user profile (optionally including a PDF resume).
- Uses the Gemini model to extract skills, experiences, and interests.
- Returns a detailed narrative description.

### 💼 Career Suggestion Agent
- Produces at least two recommended career roles.
- Includes justification, required skills, and steps for progression.
- Supports fallback parsing in case of LLM JSON failures.

### 🎓 Learning Path Generator
- Provides a complete learning plan for a chosen role, including:
  - Technologies
  - Modules
  - Duration
  - Recommended courses (Udemy / YouTube / Coursera)
  - Progression roadmap

### 📄 Resume Advisor (RAG-Powered)
- Uses a FAISS vectorstore
- Employs all-MiniLM-L6-v2 embeddings
- Performs similarity search on a local `resume_tips.txt` file
- Produces targeted resume improvements by combining RAG context + LLM reasoning

### 🗣️ Mock Interview Agent
- Generates realistic mock interview questions
- Provides model answers and improvement tips
- Adapts to the user profile & chosen role (with RAG support)

### 🧭 Personalized Learning Agent
- Extracts skill gaps
- Builds a personalized learning plan using `learning_style` & `career_goals`
- Generates skill keywords and queries SerpAPI for online courses
- Saves user preferences to a JSON file

---

## 🧩 LangGraph Architecture
The system consists of **3 separate LangGraph pipelines**:

- **Default Flow**:  
  `Profile → Role Suggestions → Learning Path`

- **Personalized Flow**:  
  `Profile → Role Suggestions → Personalized Learning (with skill gaps & preferences)`

- **Interview Flow**:  
  `Profile → Role Suggestions → Resume Feedback (RAG) → Mock Interview`

---

## 📊 Presentation

A visual overview of the Career Advisor Pipeline is available in the accompanying presentation file:

- **[Career Advisor Pipeline Presentation (PDF/Slides)](./Presentation.pdf)**
