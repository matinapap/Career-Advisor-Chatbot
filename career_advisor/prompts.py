"""Prompt builders for the Career Advisor agents."""

from __future__ import annotations

from career_advisor.llm import schema_instructions
from career_advisor.schemas import CareerSuggestions, SkillKeywords


def analyze_profile_prompt(user_profile: str) -> str:
    return f"""
Ανάλυσε σύντομα το παρακάτω προφίλ χρήστη στα ελληνικά.
Δώσε έως 6 bullets για δεξιότητες, γνώσεις, εμπειρία και ενδιαφέροντα.

Προφίλ:
{user_profile}
"""


def career_suggestions_prompt(skills_summary: str) -> str:
    return f"""
Με βάση τις παρακάτω δεξιότητες, πρότεινε ακριβώς 2 κατάλληλους επαγγελματικούς
ρόλους. Απάντησε μόνο με έγκυρο JSON που ταιριάζει στο schema.

Schema:
{schema_instructions(CareerSuggestions)}

Δεξιότητες:
{skills_summary}
"""


def learning_path_prompt(role: str) -> str:
    return f"""
Πρότεινε σύντομο πλάνο εκμάθησης για τον ρόλο: {role}.
Δώσε 4 ενότητες με τεχνολογίες, έννοιες, προτεινόμενα μαθήματα και εκτιμώμενο χρόνο.
"""


def resume_feedback_prompt(resume_text: str, context: str) -> str:
    return f"""
Αξιολόγησε το παρακάτω βιογραφικό στα ελληνικά.
Δώσε σύντομη απάντηση με: 3 δυνατά σημεία, 3 βελτιώσεις, και 2 παραδείγματα κειμένου.

Βιογραφικό:
{resume_text}

Οδηγίες / Συμπληρωματικό context:
{context}
"""


def interview_prompt(
    user_profile: str,
    chosen_role: str,
    skills_summary: str,
    rag_context: str,
) -> str:
    return f"""
Δημιούργησε μια mock συνέντευξη για τον χρήστη με βάση τα παρακάτω στοιχεία.
Δώσε 5 ερωτήσεις, σύντομες ενδεικτικές απαντήσεις και 1 tip ανά ερώτηση.

Προφίλ:
{user_profile}

Ρόλος:
{chosen_role}

Δεξιότητες:
{skills_summary}

Βιογραφικό / context:
{rag_context}
"""


def skill_gap_prompt(user_skills_text: str, role_description: str) -> str:
    return f"""
Σύγκρινε τις δεξιότητες του χρήστη με τις απαιτήσεις του ρόλου.

--- Δεξιότητες Χρήστη ---
{user_skills_text}

--- Περιγραφή Ρόλου ---
{role_description}

Βρες έως 5 σημαντικότερα gaps και δώσε σύντομη προτεραιότητα μάθησης.
"""


def personalized_learning_prompt(
    target_role: str,
    learning_style: str,
    career_goals: str,
    skill_gaps: str,
) -> str:
    return f"""
Ο χρήστης θέλει να γίνει: {target_role}
Learning style: {learning_style}
Career goals: {career_goals}

Βοήθησέ τον να μάθει ό,τι του λείπει:
{skill_gaps}

Φτιάξε σύντομο πλάνο εκμάθησης 4 εβδομάδων με θεματικές, τεχνολογίες και χρόνο ανά θέμα.
"""


def skill_keywords_prompt(skill_gaps: str, target_role: str) -> str:
    return f"""
Από την ανάλυση δεξιοτήτων εξάγαγε έως 4 σημαντικές δεξιότητες ως σύντομα
αγγλικά keywords. Απάντησε μόνο με έγκυρο JSON που ταιριάζει στο schema.

Schema:
{schema_instructions(SkillKeywords)}

Skill gaps:
{skill_gaps}

Ρόλος:
{target_role}
"""
