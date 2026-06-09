"""Configuration helpers for the Career Advisor app.

The module is intentionally Colab-friendly while still working locally.
Secrets are read from environment variables first, then from Colab userdata
when the code is running inside Google Colab.
"""

from __future__ import annotations

from pathlib import Path
import os


PACKAGE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PACKAGE_DIR.parent
DATA_DIR = PROJECT_ROOT / "career_advisor_files"

PREFS_FILE = DATA_DIR / "user_personalization.json"
RESUME_TIPS_PATH = DATA_DIR / "resume_tips.txt"

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "hf").lower()
HF_MODEL_ID = os.getenv("HF_MODEL_ID", "Qwen/Qwen2.5-0.5B-Instruct")
HF_MAX_NEW_TOKENS = int(os.getenv("HF_MAX_NEW_TOKENS", "256"))
HF_INPUT_MAX_TOKENS = int(os.getenv("HF_INPUT_MAX_TOKENS", "2048"))
HF_TEMPERATURE = float(os.getenv("HF_TEMPERATURE", "0.2"))
HF_TOP_P = float(os.getenv("HF_TOP_P", "0.9"))
HF_USE_4BIT = os.getenv("HF_USE_4BIT", "true").lower() in {"1", "true", "yes"}

GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "gemini-flash-latest")


def get_secret(name: str, colab_name: str | None = None) -> str | None:
    """Return a secret from env vars or Colab userdata."""
    value = os.getenv(name)
    if value:
        return value

    try:
        from google.colab import userdata

        return userdata.get(colab_name or name)
    except Exception:
        return None


def get_gemini_api_key() -> str | None:
    return get_secret("GEMINI_API_KEY", "Gemini_Key")


def get_serpapi_key() -> str | None:
    return get_secret("SERPAPI_KEY")
