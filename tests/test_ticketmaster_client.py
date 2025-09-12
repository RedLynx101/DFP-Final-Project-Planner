"""
Title: Ticketmaster Client Tests
Team: Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks
Date: 2025-09-12
Summary: Verifies behavior without an API key, and structure with a key (skipped if not set).
Disclaimer: This file includes AI-assisted content (GPT-5); reviewed and approved by the Purple Turtles team.
"""

import os
from datetime import datetime, timedelta

import pytest

from src.services.ticketmaster_client import fetch_events_ticketmaster


def test_ticketmaster_no_key_returns_empty():
    # Unset key in environment for this test context (do not mutate global settings file)
    key = os.getenv("TICKETMASTER_API_KEY", "")
    try:
        if key:
            os.environ["TICKETMASTER_API_KEY"] = "changeme-ticketmaster-key"
        data = fetch_events_ticketmaster(city="Pittsburgh")
        assert "events" in data
        assert isinstance(data["events"], list)
        assert len(data["events"]) == 0
    finally:
        if key:
            os.environ["TICKETMASTER_API_KEY"] = key


@pytest.mark.external
def test_ticketmaster_with_key_smoke():
    key = os.getenv("TICKETMASTER_API_KEY")
    if not key or key.startswith("changeme"):
        pytest.skip("TICKETMASTER_API_KEY not set")

    start = datetime.utcnow()
    end = start + timedelta(days=2)
    data = fetch_events_ticketmaster(city="Pittsburgh", start=start, end=end, size=10)
    assert "events" in data
    assert isinstance(data["events"], list)
    # Structure checks when present
    if data["events"]:
        e = data["events"][0]
        assert "title" in e
        assert "url" in e
        assert "source" in e and e["source"] == "ticketmaster"


