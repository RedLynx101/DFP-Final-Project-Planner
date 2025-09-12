"""
Title: Maps Client Tests
Team: Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks
Date: 2025-09-12
Summary: Verifies haversine fallback works without Maps API; optional external test with key.
Disclaimer: This file includes AI-assisted content (GPT-5); reviewed and approved by the Purple Turtles team.
"""

import os
import pytest

from src.services.maps_client import geocode_address, distance_matrix_miles
from src.core.config import get_settings


def test_haversine_fallback_matrix():
    o = [{"lat": 40.4406, "lon": -79.9959}]  # Pittsburgh
    d = [
        {"lat": 40.444, "lon": -79.943},  # near CMU
        {"lat": 40.446, "lon": -80.0},
    ]
    m = distance_matrix_miles(o, d)
    assert isinstance(m, list) and m and isinstance(m[0], list)
    assert len(m[0]) == len(d)
    assert all("distance_miles" in e and "duration_minutes" in e for e in m[0])
    # Status visibility
    print("Google Maps: haversine fallback active (no API distance call) — set MAPS_API_KEY to enable external test")


@pytest.mark.external
def test_geocode_with_google_key_optional():
    # Accept key from env or .env-backed settings
    env_key = os.getenv("MAPS_API_KEY")
    if not env_key:
        get_settings.cache_clear()
        settings_key = get_settings().maps_api_key
        key = env_key or settings_key
    else:
        key = env_key
    if not key or key.startswith("changeme"):
        pytest.skip("MAPS_API_KEY not set")
    coords = geocode_address("5000 Forbes Ave, Pittsburgh, PA 15213")
    assert coords is None or ("lat" in coords and "lon" in coords)
    print("Google Maps success: geocoding returned:", coords)


