"""Preference helpers."""

from __future__ import annotations

import json

from career_advisor.config import DATA_DIR, PREFS_FILE


def init_preferences_file() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if PREFS_FILE.exists():
        return
    save_user_preferences(
        learning_style="visual",
        career_goals="Να εργάζομαι εξ αποστάσεως και να έχω ευέλικτο ωράριο.",
    )


def save_user_preferences(learning_style: str, career_goals: str) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    payload = {"learning_style": learning_style, "career_goals": career_goals}
    PREFS_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def load_personalization_preferences() -> tuple[str, str]:
    init_preferences_file()
    try:
        prefs = json.loads(PREFS_FILE.read_text(encoding="utf-8"))
    except Exception:
        return "visual", ""
    return prefs.get("learning_style", "visual"), prefs.get("career_goals", "")
