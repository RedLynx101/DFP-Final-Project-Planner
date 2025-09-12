"""
Title: Environment Classifier (Heuristic + Optional OpenAI)
Team: Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks
Date: 2025-09-11
Summary: Classifies items as indoor/outdoor/either using keywords with optional OpenAI refinement.
Disclaimer: This file includes AI-assisted content (GPT-5); reviewed and approved by the Purple Turtles team.
"""

from __future__ import annotations

from typing import Optional

from ..core.config import get_settings


INDOOR_WORDS = {
    "museum",
    "gallery",
    "indoor",
    "theater",
    "theatre",
    "concert hall",
    "venue",
    "exhibit",
    "exhibition",
}

OUTDOOR_WORDS = {
    "park",
    "trail",
    "outdoor",
    "festival",
    "market",
    "parade",
    "riverfront",
    "outdoors",
    "hike",
    "walk",
}


def classify_environment_heuristic(text: str) -> str:
    lowered = text.lower()
    indoor = any(w in lowered for w in INDOOR_WORDS)
    outdoor = any(w in lowered for w in OUTDOOR_WORDS)
    if indoor and not outdoor:
        return "indoor"
    if outdoor and not indoor:
        return "outdoor"
    return "unknown"


def classify_environment(text: str) -> str:
    # Heuristic first
    guess = classify_environment_heuristic(text)
    if guess != "unknown":
        return guess

    # Optional OpenAI refinement
    settings = get_settings()
    key = settings.openai_api_key
    if not key or key.startswith("changeme"):
        return "unknown"

    try:
        from openai import OpenAI

        client = OpenAI(api_key=key)
        prompt = (
            "Classify the environment for this event as strictly 'indoor' or 'outdoor'. "
            "If truly unclear, return 'unknown'. Text: " + text[:800]
        )
        resp = client.chat.completions.create(
            model="gpt-oss-20b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=3,
        )
        content = resp.choices[0].message.content.strip().lower()
        if "indoor" in content:
            return "indoor"
        if "outdoor" in content:
            return "outdoor"
        return "unknown"
    except Exception:
        return "unknown"

