"""
Title: Planner Options Tests
Team: Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks
Date: 2025-09-11
Summary: Tests for POST /api/itinerary/options, fallback behavior, and schema.
Disclaimer: This file includes AI-assisted content (GPT-5); reviewed and approved by the Purple Turtles team.
"""

from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from src.main import app


client = TestClient(app)


def test_itinerary_options_endpoint_basic():
    payload = {
        "city": "Pittsburgh, PA",
        "start_date": datetime.utcnow().isoformat(),
        "end_date": (datetime.utcnow() + timedelta(days=1)).isoformat(),
        "preferences": {"budget_level": "medium", "interests": ["food"], "mobility": "walk"},
        "user_address": "5000 Forbes Ave, Pittsburgh, PA 15213",
        "max_distance_miles": 10,
    }
    resp = client.post("/api/itinerary/options", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "options" in data
    assert isinstance(data["options"], list)
    # zero or more options depending on external APIs; schema must hold


def test_single_plan_endpoint_backwards_compat():
    payload = {
        "city": "Pittsburgh, PA",
        "start_date": datetime.utcnow().isoformat(),
        "end_date": (datetime.utcnow() + timedelta(days=1)).isoformat(),
        "preferences": {"budget_level": "medium", "interests": ["museums"], "mobility": "walk"},
        "user_address": "4900 Centre Ave, Pittsburgh, PA 15213",
        "max_distance_miles": 8,
    }
    resp = client.post("/api/itinerary", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "days" in data and isinstance(data["days"], list)

