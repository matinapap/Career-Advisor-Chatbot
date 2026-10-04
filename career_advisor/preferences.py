"""Default personalization preferences.

Preferences are kept per Gradio session rather than in a shared file, so one
user's career goals are never shown to the next user of a shared demo link.
"""

from __future__ import annotations


DEFAULT_LEARNING_STYLE = "visual"
DEFAULT_CAREER_GOALS = "Να εργάζομαι εξ αποστάσεως και να έχω ευέλικτο ωράριο."


def default_personalization_preferences() -> tuple[str, str]:
    return DEFAULT_LEARNING_STYLE, DEFAULT_CAREER_GOALS
