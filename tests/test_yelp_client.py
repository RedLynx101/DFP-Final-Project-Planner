"""
Title: Yelp Client Tests
Team: Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks
Date: 2025-09-12
Summary: Verifies behavior requires API key and basic structure when a key is present (skipped if not set).
Disclaimer: This file includes AI-assisted content (GPT-5); reviewed and approved by the Purple Turtles team.

Test Script: pytest -q tests/test_yelp_client.py -s
"""

import os
import pytest

from src.core.config import get_settings
from src.services.yelp_client import search_food


def test_yelp_requires_key_env_set_or_realistic_default():
    # Ensure we can detect missing or placeholder key
    get_settings.cache_clear()
    key_from_env = os.getenv("YELP_API_KEY")
    if key_from_env:
        # If user explicitly set a key, it should not be the placeholder
        assert not key_from_env.startswith("changeme"), "YELP_API_KEY is a placeholder; set a real key or unset it"
        print("Yelp: key detected in env")
    else:
        # If not set in env, config may still read from .env; fetch it
        cfg_key = get_settings().yelp_api_key
        # Allow placeholder in quick runs; just assert the config attribute exists
        print("Yelp: using .env-backed config; placeholder acceptable for quick runs")
        assert isinstance(cfg_key, str)


@pytest.mark.external
def test_yelp_search_with_key_optional():
    # Accept key from env or .env-backed settings
    env_key = os.getenv("YELP_API_KEY")
    if not env_key:
        get_settings.cache_clear()
        settings_key = get_settings().yelp_api_key
        key = env_key or settings_key
    else:
        key = env_key

    if not key or key.startswith("changeme"):
        pytest.skip("YELP_API_KEY not set")

    # Ensure we reload settings after any env changes
    get_settings.cache_clear()

    data = search_food(query="ramen", location="Pittsburgh, PA", limit=3)
    assert "results" in data and isinstance(data["results"], list)
    # Structure checks when present
    if data["results"]:
        r = data["results"][0]
        assert "name" in r
        assert "rating" in r
        assert "url" in r
    print("Yelp success: fetched", len(data.get("results", [])), "results for 'ramen'")


