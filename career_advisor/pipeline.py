"""LangGraph pipeline orchestration."""

from __future__ import annotations

from typing import Optional, TypedDict

from langgraph.graph import END, StateGraph

from career_advisor.agents import (
    analyze_profile,
    first_suggested_role,
    format_career_suggestions,
    interview_agent,
    personalized_learning,
    suggest_careers_structured,
    suggest_learning_path,
    suggest_resume_improvements,
)
from career_advisor.pdf import extract_text_from_pdf
from career_advisor.preferences import (
    load_personalization_preferences,
    save_user_preferences,
)
from career_advisor.text_utils import clean_output


class AgentState(TypedDict):
    profile: str
    resume_text: str
    role: str
    skills: str
    suggested_roles: str
    learning_plan: str
    resume_feedback: str
    interview_questions: str
    learning_style: str
    career_goals: str


def node_wrapper(output_key, func, *input_keys):
    def wrapper(state: AgentState):
        try:
            inputs = [state.get(key, "") for key in input_keys]
            state[output_key] = func(*inputs)
        except Exception as exc:
            state[output_key] = f"(Σφάλμα στο {output_key}: {exc})"
        return state

    return wrapper


def suggest_roles_node(state: AgentState):
    suggestions = suggest_careers_structured(state.get("skills", ""))
    state["suggested_roles"] = format_career_suggestions(suggestions)
    if not state.get("role"):
        state["role"] = first_suggested_role(suggestions)
    return state


def resume_feedback_node(state: AgentState):
    if state.get("resume_text"):
        state["resume_feedback"] = suggest_resume_improvements(state["resume_text"])
    else:
        state["resume_feedback"] = "(Δεν υποβλήθηκε βιογραφικό)"
    return state


analyze_profile_node = node_wrapper("skills", analyze_profile, "profile")
learning_path_node = node_wrapper("learning_plan", suggest_learning_path, "role")
personalized_learning_node = node_wrapper(
    "learning_plan",
    lambda skills, role, learning_style, career_goals: personalized_learning(
        skills,
        role,
        {"learning_style": learning_style, "career_goals": career_goals},
    ),
    "skills",
    "role",
    "learning_style",
    "career_goals",
)
interview_node = node_wrapper(
    "interview_questions",
    lambda profile, role, resume_text, skills: interview_agent(
        profile,
        role,
        resume_text or profile,
        skills,
    ),
    "profile",
    "role",
    "resume_text",
    "skills",
)


def build_graph(nodes, edges):
    builder = StateGraph(AgentState)
    for node_name, node_func in nodes:
        builder.add_node(node_name, node_func)
    for source, target in edges:
        builder.add_edge(source, target)
    builder.set_entry_point(nodes[0][0])
    return builder.compile()


default_graph = build_graph(
    [
        ("AnalyzeProfile", analyze_profile_node),
        ("SuggestRoles", suggest_roles_node),
        ("LearningPath", learning_path_node),
    ],
    [("AnalyzeProfile", "SuggestRoles"), ("SuggestRoles", "LearningPath"), ("LearningPath", END)],
)
personalized_graph = build_graph(
    [
        ("AnalyzeProfile", analyze_profile_node),
        ("SuggestRoles", suggest_roles_node),
        ("PersonalizedLearning", personalized_learning_node),
    ],
    [
        ("AnalyzeProfile", "SuggestRoles"),
        ("SuggestRoles", "PersonalizedLearning"),
        ("PersonalizedLearning", END),
    ],
)
interview_graph = build_graph(
    [
        ("AnalyzeProfile", analyze_profile_node),
        ("SuggestRoles", suggest_roles_node),
        ("ResumeFeedback", resume_feedback_node),
        ("Interview", interview_node),
    ],
    [
        ("AnalyzeProfile", "SuggestRoles"),
        ("SuggestRoles", "ResumeFeedback"),
        ("ResumeFeedback", "Interview"),
        ("Interview", END),
    ],
)


def full_pipeline(
    user_profile: str,
    chosen_role: str = "",
    resume_file=None,
    session_state: Optional[dict] = None,
    mode: str = "default",
    learning_style: Optional[str] = None,
    career_goals: Optional[str] = None,
    personalized: bool = False,
):
    learning_style_default, career_goals_default = load_personalization_preferences()
    learning_style = learning_style or learning_style_default
    career_goals = career_goals or career_goals_default

    resume_text = ""
    if resume_file:
        resume_path = getattr(resume_file, "name", resume_file)
        resume_text = clean_output(extract_text_from_pdf(resume_path))
        user_profile = f"{user_profile}\n\n{resume_text}"

    initial_state: AgentState = {
        "profile": user_profile,
        "resume_text": resume_text,
        "role": chosen_role or "",
        "skills": "",
        "suggested_roles": "",
        "learning_plan": "",
        "resume_feedback": "",
        "interview_questions": "",
        "learning_style": learning_style,
        "career_goals": career_goals,
    }

    if mode == "default":
        final_state = default_graph.invoke(initial_state)
        if chosen_role.strip():
            result_markdown = f"""
## 🧠 Ανάλυση Δεξιοτήτων
{final_state['skills']}

## 🎓 Προτεινόμενο Πλάνο Εκμάθησης
{final_state['learning_plan']}
"""
        else:
            result_markdown = f"""
## 🧠 Ανάλυση Δεξιοτήτων
{final_state['skills']}

## 💼 Προτεινόμενοι Ρόλοι
{final_state['suggested_roles']}
"""
    elif mode == "personalized":
        final_state = personalized_graph.invoke(initial_state)
        save_user_preferences(learning_style, career_goals)
        result_markdown = final_state["learning_plan"]
    elif mode == "interview":
        final_state = interview_graph.invoke(initial_state)
        result_markdown = "\n\n".join(
            [
                f"## ✍️ Σχόλια για το Βιογραφικό\n{final_state.get('resume_feedback')}",
                f"## 🎤 Mock Συνέντευξη\n{final_state.get('interview_questions')}",
            ]
        )
    else:
        final_state = initial_state
        result_markdown = "⚠️ Μη υποστηριζόμενη λειτουργία."

    return result_markdown, final_state
