import pytest

from career_advisor.pipeline import node_wrapper, resume_feedback_node, suggest_roles_node
from career_advisor.schemas import CareerRole, CareerSuggestions


def test_node_wrapper_writes_successful_output():
    node = node_wrapper("skills", lambda profile: profile.upper(), "profile")
    state = {"profile": "python"}

    result = node(state)

    assert result["skills"] == "PYTHON"


def test_node_wrapper_raises_node_errors():
    def fail(_profile):
        raise RuntimeError("boom")

    node = node_wrapper("skills", fail, "profile")

    with pytest.raises(RuntimeError, match="skills"):
        node({"profile": "python"})


def test_suggest_roles_node_uses_structured_first_role(monkeypatch):
    suggestions = CareerSuggestions(
        roles=[
            CareerRole(
                title="AI Engineer",
                why_it_fits="Matches the profile.",
                required_skills=["Python"],
                next_steps=["Build an ML project."],
            )
        ]
    )
    monkeypatch.setattr(
        "career_advisor.pipeline.suggest_careers_structured",
        lambda _skills: suggestions,
    )

    state = {"skills": "Python", "role": ""}
    result = suggest_roles_node(state)

    assert result["role"] == "AI Engineer"
    assert "AI Engineer" in result["suggested_roles"]


def test_resume_feedback_node_handles_missing_resume():
    result = resume_feedback_node({"resume_text": ""})

    assert result["resume_feedback"] == "(Δεν υποβλήθηκε βιογραφικό)"
