"""
Title: Weather Client Tests
Team: Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks
Date: 2025-09-12
Summary: Unit tests for outdoor suitability and mapping; optional external fetch with
        clear API key status reporting.
Disclaimer: This file includes AI-assisted content (GPT-5); reviewed and approved by the Purple Turtles team.
"""

import os
import pytest

from src.services.weather_client import outdoor_suitability, map_forecast_to_days, fetch_forecast
from src.core.config import get_settings


def test_outdoor_suitability_scoring():
    good = outdoor_suitability({"temp_f": 72, "wind_mph": 5, "precip_prob": 0.05})
    bad = outdoor_suitability({"temp_f": 35, "wind_mph": 30, "precip_prob": 0.9})
    assert good > bad
    assert 0.0 <= good <= 1.0
    assert 0.0 <= bad <= 1.0


def test_weather_key_status_report():
    """Always-run status report to indicate OpenWeather key presence.

    Prints a human-friendly status when run with -s.
    """
    get_settings.cache_clear()
    env_key = os.getenv("WEATHER_API_KEY")
    cfg_key = get_settings().weather_api_key
    key = env_key or cfg_key
    is_placeholder = (not key) or key.startswith("changeme")
    if is_placeholder:
        print("OpenWeather: disabled (no key or placeholder)")
    else:
        print("OpenWeather: key detected; external fetch tests available via -m external")
    assert True


@pytest.mark.external
def test_fetch_forecast_optional():
    # Accept key from env or .env-backed settings
    env_key = os.getenv("WEATHER_API_KEY")
    if not env_key:
        get_settings.cache_clear()
        settings_key = get_settings().weather_api_key
        key = env_key or settings_key
    else:
        key = env_key
    if not key or key.startswith("changeme"):
        pytest.skip("WEATHER_API_KEY not set")

    # Ensure we reload settings with the final value in effect
    get_settings.cache_clear()

    try:
        data = fetch_forecast("Pittsburgh, PA")
    except Exception as e:
        # Gracefully skip on auth issues so suite remains green when key is invalid
        msg = str(e)
        if "401" in msg or "Unauthorized" in msg:
            pytest.skip("OpenWeather key present but unauthorized (401); verify key")
        raise
    days = map_forecast_to_days(data)
    assert isinstance(days, dict)
    # Helpful runtime context when run with -s
    list_count = len(data.get("list", [])) if isinstance(data, dict) else 0
    print("OpenWeather success: fetched", list_count, "3-hour entries; days summarized:", len(days))
    if days:
        first_day = sorted(days.keys())[0]
        sample = days[first_day]
        print("Sample day:", {"date": first_day, **{k: sample.get(k) for k in ("temp_avg_f", "wind_avg_mph", "precip_prob_avg", "suitability")}})


