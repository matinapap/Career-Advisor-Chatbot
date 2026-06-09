"""Career Advisor agent functions."""

from __future__ import annotations

from typing import Optional

from career_advisor.courses import search_courses
from career_advisor.llm import llm_run, llm_run_json
from career_advisor.prompts import (
    analyze_profile_prompt,
    career_suggestions_prompt,
    interview_prompt,
    learning_path_prompt,
    personalized_learning_prompt,
    resume_feedback_prompt,
    role_description_prompt,
    skill_gap_prompt,
    skill_keywords_prompt,
)
from career_advisor.rag import search_resume_tips
from career_advisor.schemas import CareerRole, CareerSuggestions, SkillKeywords
from career_advisor.text_utils import clean_output


def analyze_profile(user_profile: str) -> str:
    return llm_run(analyze_profile_prompt(user_profile))


def suggest_careers_structured(skills_summary: str) -> CareerSuggestions:
    """Return role suggestions as validated structured data."""
    try:
        suggestions = llm_run_json(
            career_suggestions_prompt(skills_summary),
            CareerSuggestions,
        )
    except Exception as exc:
        return CareerSuggestions(
            roles=[
                CareerRole(
                    title="No role",
                    why_it_fits=f"Δεν ήταν δυνατή η δομημένη παραγωγή ρόλων: {exc}",
                    required_skills=[],
                    next_steps=["Δοκίμασε ξανά με πιο αναλυτικό προφίλ."],
                )
            ]
        )

    roles = suggestions.roles[:2]
    if not roles:
        return CareerSuggestions(
            roles=[
                CareerRole(
                    title="No role",
                    why_it_fits="Το μοντέλο δεν επέστρεψε προτεινόμενους ρόλους.",
                    required_skills=[],
                    next_steps=["Δοκίμασε ξανά με πιο αναλυτικό προφίλ."],
                )
            ]
        )
    return CareerSuggestions(roles=roles)


def format_career_suggestions(suggestions: CareerSuggestions) -> str:
    if not suggestions.roles:
        return "(Δεν βρέθηκαν προτεινόμενοι ρόλοι.)"

    sections = []
    for index, role in enumerate(suggestions.roles, start=1):
        required_skills = "\n".join(f"- {skill}" for skill in role.required_skills)
        next_steps = "\n".join(f"- {step}" for step in role.next_steps)
        sections.append(
            f"""
**{index}. {role.title}**

**Γιατί ταιριάζει:** {role.why_it_fits}

**Απαραίτητες δεξιότητες:**
{required_skills or "- Δεν δόθηκαν δεξιότητες."}

**Επόμενα βήματα:**
{next_steps or "- Δεν δόθηκαν επόμενα βήματα."}
""".strip()
        )
    return "\n\n".join(sections)


def suggest_careers(skills_summary: str) -> str:
    return format_career_suggestions(suggest_careers_structured(skills_summary))


def first_suggested_role(suggestions: CareerSuggestions) -> str:
    if suggestions.roles:
        return suggestions.roles[0].title
    return "No role"


def suggest_learning_path(role: str) -> str:
    return llm_run(learning_path_prompt(role))


def suggest_resume_improvements(resume_text: str) -> str:
    context = search_resume_tips(resume_text)
    return clean_output(llm_run(resume_feedback_prompt(resume_text, context)))


def interview_agent(user_profile: str, chosen_role: str, resume_text: Optional[str] = None) -> str:
    skills_summary = analyze_profile(user_profile)
    rag_context = search_resume_tips(resume_text or user_profile)
    prompt = interview_prompt(user_profile, chosen_role, skills_summary, rag_context)
    return clean_output(llm_run(prompt))


def extract_skill_keywords(skill_gaps: str, target_role: str) -> list[str]:
    """Return skill keywords from validated LLM JSON, with a conservative fallback."""
    try:
        keywords = llm_run_json(
            skill_keywords_prompt(skill_gaps, target_role),
            SkillKeywords,
        )
        skills = [skill.strip() for skill in keywords.skills if skill.strip()]
        return skills[:4] or ["python", "sql", "data analysis", "excel"]
    except Exception:
        return ["python", "sql", "data analysis", "excel"]


def personalized_learning(user_skills_text: str, target_role: str, personalization_info: dict) -> str:
    role_description = llm_run(role_description_prompt(target_role))
    skill_gaps = llm_run(skill_gap_prompt(user_skills_text, role_description))
    learning_plan = llm_run(
        personalized_learning_prompt(
            target_role=target_role,
            learning_style=personalization_info.get("learning_style", "-"),
            career_goals=personalization_info.get("career_goals", "-"),
            skill_gaps=skill_gaps,
        )
    )

    courses_output = ""
    for skill in extract_skill_keywords(skill_gaps, target_role):
        courses_output += f"### {skill}\n{search_courses(skill)}\n\n"

    return f"""
## 🎯 Ρόλος: {target_role}

## 🔎 Ανάλυση Skill Gaps
{skill_gaps}

---

## 🎓 Προσωποποιημένο Πλάνο Εκμάθησης
{learning_plan}

---

## 🎓 Προτεινόμενα Μαθήματα
{courses_output}
"""
