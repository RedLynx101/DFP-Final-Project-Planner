"""
Title: Environment Classifier (Heuristic + Optional OpenAI)
Team: Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks
Date: 2025-09-11
Summary: Classifies items as indoor/outdoor/either using keywords with optional OpenAI refinement.
Disclaimer: This file includes AI-assisted content (GPT-5); reviewed and approved by the Purple Turtles team.
"""

from __future__ import annotations

from typing import Optional
import json

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
    "arena",
    "center",
    "centre",
    "hall",
    "gym",
    "aquarium",
    "arcade",
    "bowling",
    "brewery",
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
    "garden",
    "playground",
    "plaza",
    "zoo",
    "waterfront",
    "beach",
}


def classify_environment_heuristic(text: str) -> str:
    lowered = text.lower()
    # Score by counts to break ties instead of returning unknown when both present
    indoor_count = sum(lowered.count(w) for w in INDOOR_WORDS)
    outdoor_count = sum(lowered.count(w) for w in OUTDOOR_WORDS)
    if indoor_count > outdoor_count:
        return "indoor"
    if outdoor_count > indoor_count:
        return "outdoor"
    # As a last resort, look for exact tokens at start/end
    tokens = set(lowered.replace("-", " ").split())
    if tokens & INDOOR_WORDS and not (tokens & OUTDOOR_WORDS):
        return "indoor"
    if tokens & OUTDOOR_WORDS and not (tokens & INDOOR_WORDS):
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
        system = (
            "You are an environment classifier. Return only a JSON object with a 'label' "
            "field that is either 'indoor' or 'outdoor'. Choose the most plausible one; "
            "do not output 'unknown'. Hints: museum, gallery, arena, center, hall => indoor; "
            "park, trail, garden, playground, outdoor market => outdoor."
        )
        user = (
            "Classify the following text. Return JSON only. Text: " + text[:800]
        )
        # Ask for a single-word answer; models often follow this reliably.
        resp = client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": (
                    "Answer with exactly one word: 'indoor' or 'outdoor'. No punctuation or extra words."
                )},
                {"role": "user", "content": user},
            ],
            max_completion_tokens=settings.openai_max_completion_tokens,
        )
        content = (resp.choices[0].message.content or "").strip().lower()
        if content in {"indoor", "outdoor"}:
            return content

        # Final fallback: keep unknown if model didn't comply
        return "unknown"
    except Exception:
        return "unknown"

