"""Course search integration."""

from __future__ import annotations

import logging

import requests

from career_advisor.config import get_serpapi_key


logger = logging.getLogger(__name__)


def search_courses(skill: str, max_results: int = 3) -> str:
    api_key = get_serpapi_key()
    if not api_key:
        return (
            "Live course search is not enabled right now because SERPAPI_KEY "
            "has not been configured."
        )

    platforms = ["udemy.com", "coursera.org", "youtube.com"]
    results_out = []
    for site in platforms:
        query = f"{skill} course site:{site}"
        try:
            response = requests.get(
                "https://serpapi.com/search.json",
                params={"q": query, "api_key": api_key, "num": max_results},
                timeout=8,
            )
            if response.status_code != 200:
                logger.warning(
                    "SerpAPI request failed for site=%s with status=%s.",
                    site,
                    response.status_code,
                )
                continue
            for item in response.json().get("organic_results", [])[:max_results]:
                title = item.get("title")
                link = item.get("link")
                if title and link:
                    results_out.append(f"- [{title}]({link})")
        except requests.RequestException:
            logger.exception("SerpAPI request failed for site=%s.", site)
            continue
    return "\n".join(results_out) if results_out else f"(No courses found for: {skill})"
