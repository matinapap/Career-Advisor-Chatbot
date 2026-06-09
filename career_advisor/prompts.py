"""Prompt builders for the Career Advisor agents."""

from __future__ import annotations

from career_advisor.llm import schema_instructions
from career_advisor.schemas import CareerSuggestions, SkillKeywords


def analyze_profile_prompt(user_profile: str) -> str:
    return f"""
Ανάλυσε το παρακάτω προφίλ χρήστη και γράψε ένα αναλυτικό κείμενο στα ελληνικά
που περιγράφει τις δεξιότητες, γνώσεις και ενδιαφέροντα του χρήστη.

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
Πρότεινε ένα αναλυτικό πλάνο εκμάθησης για τον ρόλο: {role}.
Συμπερίλαβε τεχνολογίες, έννοιες, προτεινόμενα online μαθήματα
και εκτιμώμενο χρόνο για κάθε θέμα.
"""


def resume_feedback_prompt(resume_text: str, context: str) -> str:
    return f"""
Αξιολόγησε το παρακάτω βιογραφικό και δώσε αναλυτικά σχόλια στα ελληνικά.
Συμπεριέλαβε τι λειτουργεί καλά, τι όχι, προτάσεις ανά ενότητα και συγκεκριμένο
κείμενο που μπορεί να προστεθεί ή να αντικατασταθεί.

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
Συμπεριέλαβε αναλυτικές απαντήσεις, επεξηγήσεις και tips για κάθε ερώτηση.

Προφίλ:
{user_profile}

Ρόλος:
{chosen_role}

Δεξιότητες:
{skills_summary}

Βιογραφικό / context:
{rag_context}
"""


def role_description_prompt(target_role: str) -> str:
    return f"""
Δώσε περιγραφή για τον ρόλο: {target_role}.
Περιέγραψε καθήκοντα και απαιτούμενες τεχνολογίες / δεξιότητες.
"""


def skill_gap_prompt(user_skills_text: str, role_description: str) -> str:
    return f"""
Σύγκρινε τις δεξιότητες του χρήστη με τις απαιτήσεις του ρόλου.

--- Δεξιότητες Χρήστη ---
{user_skills_text}

--- Περιγραφή Ρόλου ---
{role_description}

Βρες ποιες δεξιότητες λείπουν, πού είναι αρχάριος και τα σημαντικότερα gaps.
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

Φτιάξε πλάνο εκμάθησης με θεματικές, τεχνολογίες, μαθήματα και χρόνο ανά θέμα.
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
