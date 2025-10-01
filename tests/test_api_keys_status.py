r"""
Title: API Keys Status Report Tests
Team: Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks
Date: 2025-09-12
Summary: Always-run status prints for all potential external API keys, including unused EVENTS_API_KEY.
Disclaimer: This file includes AI-assisted content (GPT-5); reviewed and approved by the Purple Turtles team.

Test Script: .\.venv\Scripts\python -m pytest -q -s tests\test_api_keys_status.py
"""

import os

from src.core.config import get_settings


def _status(name: str, key: str | None) -> str:
    if not key or key.startswith("changeme"):
        return f"{name}: disabled (no key or placeholder)"
    return f"{name}: key detected"


def test_all_api_keys_status_report():
    """Print a concise status line for each known integration.

    This test always passes but provides feedback under -s to show which keys are active.
    """
    get_settings.cache_clear()
    s = get_settings()

    # Prefer env var if present; else use settings (which may read .env)
    keys = {
        "Ticketmaster": os.getenv("TICKETMASTER_API_KEY") or s.ticketmaster_api_key,
        "Yelp": os.getenv("YELP_API_KEY") or s.yelp_api_key,
        "OpenWeather": os.getenv("WEATHER_API_KEY") or s.weather_api_key,
        "Google Maps": os.getenv("MAPS_API_KEY") or s.maps_api_key,
        "OpenAI": os.getenv("OPENAI_API_KEY") or s.openai_api_key,
    }

    for name, key in keys.items():
        print(_status(name, key))

    # Special-case notes for integrations with graceful fallbacks
    if not keys["Google Maps"] or keys["Google Maps"].startswith("changeme"):
        print("Google Maps fallback: haversine distances active")
    if not keys["OpenWeather"] or keys["OpenWeather"].startswith("changeme"):
        print("OpenWeather: planner will skip weather-aware adjustments")

    assert True


