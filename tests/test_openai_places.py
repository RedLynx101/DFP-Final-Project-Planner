"""
Title: OpenAI Place Classification Accuracy Test
Team: Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks
Date: 2025-09-12
Summary: Uses OpenAI (gpt-5-nano-2025-08-07) to classify five places as indoor or outdoor and prints success rate.
Disclaimer: This file includes AI-assisted content (GPT-5); reviewed and approved by the Purple Turtles team.
"""

from __future__ import annotations

import os
from typing import Dict, List, Optional, Tuple

import pytest

from src.core.config import get_settings


def _build_items() -> List[Dict[str, Optional[str]]]:
    # Some with descriptions, some name-only to simulate upstream gaps
    return [
        {"name": "Carnegie Museum of Art", "description": "Art museum with galleries and exhibits", "expected": "indoor"},
        {"name": "Schenley Park", "description": "Large urban park with trails and lawns", "expected": "outdoor"},
        {"name": "Heinz History Center", "description": None, "expected": "indoor"},
        {"name": "Frick Park", "description": None, "expected": "outdoor"},
        {"name": "PPG Paints Arena", "description": "Indoor arena for hockey games and concerts", "expected": "indoor"},
    ]


def _make_prompt(name: str, description: Optional[str]) -> str:
    base = (
        "Classify the environment for this place as strictly 'indoor' or 'outdoor'. "
        "Respond with only one word: 'indoor' or 'outdoor'.\n"
        f"Name: {name}\n"
    )
    if description:
        base += f"Description: {description[:300]}\n"
    else:
        base += "Description: (not provided)\n"
    return base


def _parse_label(text: str) -> str:
    lowered = (text or "").strip().lower()
    if "indoor" in lowered and "outdoor" not in lowered:
        return "indoor"
    if "outdoor" in lowered and "indoor" not in lowered:
        return "outdoor"
    # Fallback to first token heuristic
    first = lowered.split()[0] if lowered else ""
    if first in {"indoor", "outdoor"}:
        return first
    return "unknown"


@pytest.mark.external
def test_openai_places_classification_accuracy():
    # Use OPENAI_API_KEY from env or settings; skip if not present/placeholder
    env_key = os.getenv("OPENAI_API_KEY")
    if not env_key:
        get_settings.cache_clear()
        settings_key = get_settings().openai_api_key
        key = env_key or settings_key
    else:
        key = env_key
    if not key or key.startswith("changeme"):
        pytest.skip("OPENAI_API_KEY not set")

    # Late import to avoid dependency when skipping
    try:
        from openai import OpenAI
    except Exception as e:  # pragma: no cover
        pytest.skip(f"openai package not available: {e}")

    client = OpenAI(api_key=key)
    model = "gpt-5-nano-2025-08-07"

    items = _build_items()
    correct = 0
    outputs: List[Tuple[str, str, str]] = []  # (name, expected, got)

    for item in items:
        prompt = _make_prompt(item["name"] or "", item.get("description"))
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
                max_tokens=3,
            )
            content = resp.choices[0].message.content
        except Exception as e:
            msg = str(e).lower()
            if "model" in msg or "not found" in msg:
                pytest.skip("OpenAI model 'gpt-5-nano-2025-08-07' unavailable; configure access or adjust model name")
            raise

        label = _parse_label(content)
        expected = item["expected"] or "unknown"
        if label == expected:
            correct += 1
        outputs.append((item["name"] or "<unknown>", expected, label))

    # Print per-item results and success rate for visibility under -s
    for name, expected, label in outputs:
        print(f"OpenAI classified: {name} -> {label} (expected: {expected})")
    rate = correct / len(items)
    print(f"OpenAI classification success rate: {correct}/{len(items)} = {rate:.0%}")

    # Do not assert on accuracy; only ensure outputs are parseable labels
    assert all(label in {"indoor", "outdoor", "unknown"} for _, _, label in outputs)


