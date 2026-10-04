"""PDF extraction helpers."""

from __future__ import annotations

import logging

from pypdf import PdfReader


logger = logging.getLogger(__name__)

MAX_PDF_PAGES = 10
MAX_PDF_CHARS = 20_000


def extract_text_from_pdf(pdf_path: str) -> str:
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages[:MAX_PDF_PAGES]:
            text += page.extract_text() or ""
            if len(text) >= MAX_PDF_CHARS:
                break
    except Exception:
        logger.exception("Could not read the uploaded PDF.")
        return "(Δεν ήταν δυνατή η ανάγνωση του PDF.)"
    return text[:MAX_PDF_CHARS]
