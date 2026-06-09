import pytest

from career_advisor import llm
from career_advisor.schemas import CareerSuggestions, SkillKeywords


def test_extract_json_from_fenced_response():
    raw = """
    Here is the result:
    ```json
    {"skills": ["python", "sql"]}
    ```
    """

    assert llm._extract_json(raw) == {"skills": ["python", "sql"]}


def test_extract_json_raises_for_missing_json():
    with pytest.raises(ValueError):
        llm._extract_json("No JSON here")


def test_llm_run_json_validates_schema(monkeypatch):
    monkeypatch.setattr(
        llm,
        "llm_run",
        lambda prompt: '{"skills": ["python", "machine learning"]}',
    )

    result = llm.llm_run_json("ignored", SkillKeywords)

    assert result.skills == ["python", "machine learning"]


def test_career_suggestions_schema_requires_roles():
    payload = {
        "roles": [
            {
                "title": "Data Analyst",
                "why_it_fits": "Matches the user's analytical interests.",
                "required_skills": ["SQL", "Excel"],
                "next_steps": ["Build a portfolio dashboard."],
            }
        ]
    }

    result = llm._validate_schema(CareerSuggestions, payload)

    assert result.roles[0].title == "Data Analyst"
