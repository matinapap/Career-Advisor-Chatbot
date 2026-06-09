"""Small text formatting helpers."""

from __future__ import annotations

import re


def clean_output(raw_text: str) -> str:
    if not raw_text:
        return "(No output)"
    raw_text = str(raw_text)
    if raw_text.strip().startswith(("<!DOCTYPE", "<html")):
        return re.sub(r"<[^>]*>", "", raw_text)
    return raw_text
