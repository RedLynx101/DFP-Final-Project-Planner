Title: Tests Overview
Team: Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks
Date: 2025-09-12
Summary: How to run the test suite and optional external tests. Includes API key status reporting.
Disclaimer: This document includes AI-assisted content (GPT-5); reviewed and approved by the Purple Turtles team.

## Layout

- test_smoke.py — API health + itinerary smoke
- test_api_keys_status.py — always-run status lines for API keys (Ticketmaster, Yelp, OpenWeather, Google Maps, OpenAI)
- test_planner_options.py — itinerary options and backward-compat single plan
- test_scraper.py — VisitPittsburgh scraper integration
- test_ticketmaster_client.py — Ticketmaster client
- test_yelp_client.py — Yelp Fusion client
- test_maps_client.py — Maps client
- test_weather_client.py — Weather utilities
- test_classifier.py — Heuristic classifier
- test_openai_places.py — External: classify five places via OpenAI and print success rate

## Running

Quick run (no external APIs required):
```powershell
pytest -q
```

By default, tests marked `@pytest.mark.external` are excluded via `pytest.ini`.
To run external tests, pass `-m external`:
```powershell
pytest -q -m external
```

You will see status lines for each API under `test_api_keys_status.py` when running with `-s`:
```powershell
pytest -q -s tests/test_api_keys_status.py
```
Example output:
```
Ticketmaster: disabled (no key or placeholder)
Yelp: key detected
OpenWeather: disabled (no key or placeholder)
Google Maps: key detected
OpenAI: disabled (no key or placeholder)
Events (unused): disabled (no key or placeholder)
Google Maps fallback: haversine distances active
OpenWeather: planner will skip weather-aware adjustments
```

Run only scraper:
```powershell
pytest -q tests/test_scraper.py
```

Run external tests (require API keys in environment or .env):
```powershell
pytest -q -m external
```

Run only the OpenAI places classification test:
```powershell
$env:OPENAI_API_KEY="<YOUR_KEY>"
pytest -q -m external -s tests\test_openai_places.py
```

Tips:
- Marked tests are optional: they `skip` cleanly if a real key isn't configured.
- Most external tests print helpful context when run with `-s` (e.g., counts fetched, sample objects).

Tip: You can use PowerShell to set a key for the current session:
```powershell
$env:TICKETMASTER_API_KEY="<YOUR_KEY>"
$env:YELP_API_KEY="<YOUR_KEY>"
$env:WEATHER_API_KEY="<YOUR_KEY>"
$env:MAPS_API_KEY="<YOUR_KEY>"; $env:MAPS_PROVIDER="google"
$env:OPENAI_API_KEY="<YOUR_KEY>"
```


