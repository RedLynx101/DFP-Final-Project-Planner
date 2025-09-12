"""
Title: Classifier Tests
Team: Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks
Date: 2025-09-12
Summary: Heuristic indoor/outdoor classification sanity checks.
Disclaimer: This file includes AI-assisted content (GPT-5); reviewed and approved by the Purple Turtles team.
"""

from src.services.classifier import classify_environment_heuristic


def test_classifier_heuristic_sanity():
    assert classify_environment_heuristic("Museum exhibit") == "indoor"
    assert classify_environment_heuristic("Park festival") == "outdoor"
    # Mixed or unclear text may be unknown
    assert classify_environment_heuristic("Event with food and fun") in {"indoor", "outdoor", "unknown"}


