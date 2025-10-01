"""
Title: Smoke Tests
Team: Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks
Date: 2025-09-11
Summary: Basic tests for health and itinerary endpoint.
Disclaimer: This file includes AI-assisted content (GPT-5); reviewed and approved by the Purple Turtles team.
"""

from fastapi.testclient import TestClient
from src.main import app
from datetime import datetime, timedelta, UTC


client = TestClient(app)


def test_health():
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_itinerary():
    payload = {
        "city": "Pittsburgh, PA",
        "start_date": datetime.now(UTC).isoformat(),
        "end_date": (datetime.now(UTC) + timedelta(days=1)).isoformat(),
        "preferences": {"budget_level": "low", "interests": ["food"], "mobility": "walk"},
    }
    resp = client.post("/api/itinerary", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "days" in data and len(data["days"]) >= 1


