"""PDF extraction helpers."""

from __future__ import annotations

import PyPDF2


def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ""
    except Exception as exc:
        text = f"(Σφάλμα στην ανάγνωση PDF: {exc})"
    return text
