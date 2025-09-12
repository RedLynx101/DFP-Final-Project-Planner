"""
Title: Classifier Tests
Team: Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks
Date: 2025-09-12
Summary: Heuristic indoor/outdoor classification sanity checks; optional OpenAI key status.
Disclaimer: This file includes AI-assisted content (GPT-5); reviewed and approved by the Purple Turtles team.
"""

import os
import pytest

from src.services.classifier import classify_environment_heuristic, classify_environment
from src.core.config import get_settings


def test_classifier_heuristic_sanity():
    assert classify_environment_heuristic("Museum exhibit") == "indoor"
    assert classify_environment_heuristic("Park festival") == "outdoor"
    # Mixed or unclear text may be unknown
    assert classify_environment_heuristic("Event with food and fun") in {"indoor", "outdoor", "unknown"}


def test_openai_key_status_report():
    get_settings.cache_clear()
    env_key = os.getenv("OPENAI_API_KEY")
    cfg_key = get_settings().openai_api_key
    key = env_key or cfg_key
    is_placeholder = (not key) or key.startswith("changeme")
    if is_placeholder:
        print("OpenAI: disabled (no key or placeholder)")
    else:
        print("OpenAI: key detected; optional refinement active in classify_environment")
    assert True


@pytest.mark.external
def test_openai_refinement_optional():
    env_key = os.getenv("OPENAI_API_KEY")
    if not env_key:
        get_settings.cache_clear()
        settings_key = get_settings().openai_api_key
        key = env_key or settings_key
    else:
        key = env_key
    if not key or key.startswith("changeme"):
        pytest.skip("OPENAI_API_KEY not set")

    get_settings.cache_clear()
    # Provide ambiguous text to encourage refinement use
    result = classify_environment("Community event with activities")
    print("OpenAI refinement result:", result)
    assert result in {"indoor", "outdoor", "unknown"}

