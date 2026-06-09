"""Course search integration."""

from __future__ import annotations

import requests

from career_advisor.config import get_serpapi_key


def search_courses(skill: str, max_results: int = 3) -> str:
    api_key = get_serpapi_key()
    if not api_key:
        return "ERROR: Missing SerpAPI key."

    platforms = ["udemy.com", "coursera.org", "youtube.com"]
    results_out = []
    for site in platforms:
        query = requests.utils.requote_uri(f"{skill} course site:{site}")
        url = f"https://serpapi.com/search.json?q={query}&api_key={api_key}&num={max_results}"
        try:
            response = requests.get(url, timeout=8)
            if response.status_code != 200:
                continue
            for item in response.json().get("organic_results", [])[:max_results]:
                title = item.get("title")
                link = item.get("link")
                if title and link:
                    results_out.append(f"- [{title}]({link})")
        except Exception:
            continue
    return "\n".join(results_out) if results_out else f"(Δεν βρέθηκαν courses για: {skill})"
