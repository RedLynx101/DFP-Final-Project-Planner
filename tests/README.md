Title: Tests Overview
Team: Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks
Date: 2025-09-12
Summary: How to run the test suite and optional external tests.
Disclaimer: This document includes AI-assisted content (GPT-5); reviewed and approved by the Purple Turtles team.

## Layout

- test_smoke.py — API health + itinerary smoke
- test_planner_options.py — itinerary options and backward-compat single plan
- test_scraper.py — VisitPittsburgh scraper integration
- test_ticketmaster_client.py — Ticketmaster client
- test_maps_client.py — Maps client
- test_weather_client.py — Weather utilities
- test_classifier.py — Heuristic classifier

## Running

Quick run (no external APIs required):
```powershell
pytest -q
```

Run only scraper:
```powershell
pytest -q tests/test_scraper.py
```

Run external tests (require API keys in environment or .env):
```powershell
pytest -q -m external
```

Tip: You can use PowerShell to set a key for the current session:
```powershell
$env:TICKETMASTER_API_KEY="<YOUR_KEY>"
```


