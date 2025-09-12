"""
Title: Ticketmaster Client Tests
Team: Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks
Date: 2025-09-12
Summary: Verifies behavior without an API key, and structure with a key (skipped if not set).
Disclaimer: This file includes AI-assisted content (GPT-5); reviewed and approved by the Purple Turtles team.

Warning: This test requires a valid Ticketmaster API key to run.

Test Script: pytest -q tests/test_ticketmaster_client.py -s
"""

import os
from datetime import datetime, timedelta

import pytest

from src.services.ticketmaster_client import fetch_events_ticketmaster
from src.core.config import get_settings


def test_ticketmaster_no_key_returns_empty():
    # Force a no-key scenario by overriding env, and clear cached settings
    prev = os.environ.get("TICKETMASTER_API_KEY")
    try:
        os.environ["TICKETMASTER_API_KEY"] = "changeme-ticketmaster-key"
        get_settings.cache_clear()
        data = fetch_events_ticketmaster(city="Pittsburgh")
        # Basic shape with explanatory messages
        assert "events" in data, "Ticketmaster (no key): response missing 'events' key"
        assert isinstance(data["events"], list), "Ticketmaster (no key): 'events' should be a list"
        assert len(data["events"]) == 0, "Ticketmaster (no key): expected zero events when key is unset"
        # Helpful runtime context when run with -s
        print(f"Ticketmaster: disabled (no key) — events returned = {len(data.get('events', []))}")
    finally:
        if prev is None:
            os.environ.pop("TICKETMASTER_API_KEY", None)
        else:
            os.environ["TICKETMASTER_API_KEY"] = prev
        get_settings.cache_clear()


@pytest.mark.external
def test_ticketmaster_with_key_smoke():
    # Accept key from either env or .env-backed settings
    env_key = os.getenv("TICKETMASTER_API_KEY")
    if not env_key:
        get_settings.cache_clear()
        settings_key = get_settings().ticketmaster_api_key
        key = env_key or settings_key
    else:
        key = env_key
    if not key or key.startswith("changeme"):
        pytest.skip("TICKETMASTER_API_KEY not set")

    # Ensure we reload settings with the final value in effect
    get_settings.cache_clear()

    start = datetime.utcnow()
    end = start + timedelta(days=2)
    data = fetch_events_ticketmaster(city="Pittsburgh", start=start, end=end, size=10)
    assert "events" in data, "Ticketmaster: response missing 'events' key"
    assert isinstance(data["events"], list), "Ticketmaster: 'events' should be a list"
    count = len(data.get("events", []))
    # Helpful runtime context when run with -s
    print("Ticketmaster success: fetched", count, "events for Pittsburgh between", start, "and", end)
    # Structure checks when present
    if data["events"]:
        e = data["events"][0]
        # Print a small sample for visibility under -s
        print(
            "Sample event:",
            {
                "title": e.get("title"),
                "start_datetime": e.get("start_datetime"),
                "venue": e.get("venue"),
                "url": e.get("url"),
                # Use our simplified client's 'details' as a description-like field
                "description": e.get("details"),
            },
        )
        assert "title" in e, "Ticketmaster: event missing 'title'"
        assert "url" in e, "Ticketmaster: event missing 'url'"
        assert "source" in e and e["source"] == "ticketmaster", "Ticketmaster: wrong 'source' field"


