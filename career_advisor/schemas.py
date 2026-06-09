"""Structured output schemas for LLM responses."""

from __future__ import annotations

from pydantic import BaseModel, Field


class CareerRole(BaseModel):
    title: str = Field(description="Career role title.")
    why_it_fits: str = Field(description="Why this role fits the user profile.")
    required_skills: list[str] = Field(description="Skills required for the role.")
    next_steps: list[str] = Field(description="Concrete steps the user should take next.")


class CareerSuggestions(BaseModel):
    roles: list[CareerRole] = Field(description="Two suitable career role suggestions.")


class SkillKeywords(BaseModel):
    skills: list[str] = Field(description="Up to four short English skill keywords.")
