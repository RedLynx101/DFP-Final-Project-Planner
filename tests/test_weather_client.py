"""
Title: Weather Client Tests
Team: Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks
Date: 2025-09-12
Summary: Unit tests for outdoor suitability and mapping; optional external fetch.
Disclaimer: This file includes AI-assisted content (GPT-5); reviewed and approved by the Purple Turtles team.
"""

import os
import pytest

from src.services.weather_client import outdoor_suitability, map_forecast_to_days, fetch_forecast


def test_outdoor_suitability_scoring():
    good = outdoor_suitability({"temp_f": 72, "wind_mph": 5, "precip_prob": 0.05})
    bad = outdoor_suitability({"temp_f": 35, "wind_mph": 30, "precip_prob": 0.9})
    assert good > bad
    assert 0.0 <= good <= 1.0
    assert 0.0 <= bad <= 1.0


@pytest.mark.external
def test_fetch_forecast_optional():
    key = os.getenv("WEATHER_API_KEY")
    if not key or key.startswith("changeme"):
        pytest.skip("WEATHER_API_KEY not set")
    data = fetch_forecast("Pittsburgh, PA")
    days = map_forecast_to_days(data)
    assert isinstance(days, dict)


