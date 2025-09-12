Title: Environment Setup and Testing Guide
Team: Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks
Date: 2025-09-12
Summary: Example `.env` and the recommended order to add API keys and test each integration.
Disclaimer: This document includes AI-assisted content (GPT-5); reviewed and approved by the Purple Turtles team.

## .env example

Copy the following into a new `.env` file at the repo root and fill values:

```env
# App basics
APP_NAME=weekender
ENV=development
DEBUG=true
LOG_LEVEL=INFO
PORT=8000

# 1) Ticketmaster Discovery API — API-based events
# https://developer.ticketmaster.com/
TICKETMASTER_API_KEY=

# 2) Yelp Fusion — food search
# https://www.yelp.com/developers/v3/manage_app
YELP_API_KEY=

# 3) OpenWeather — weather-aware planning
# https://home.openweathermap.org/api_keys
WEATHER_API_KEY=

# 4) Google Maps — geocoding + distance matrix
# https://console.cloud.google.com/apis/credentials
MAPS_PROVIDER=google
MAPS_API_KEY=

# Optional — OpenAI (for classifier refinement)
OPENAI_API_KEY=
```

## Recommended testing order

Pre-flight (one time):
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Note: External tests are excluded by default via `pytest.ini`. To include them, use `-m external`.

0) Baseline scraper (no keys needed):
```powershell
pytest -q tests/test_scraper.py -q
```

0.1) API keys status (no keys needed; prints what's active). Use -s to see lines:
```powershell
pytest -q -s tests/test_api_keys_status.py
```

1) Ticketmaster API (set TICKETMASTER_API_KEY):
```powershell
$env:TICKETMASTER_API_KEY="<YOUR_KEY>"
python -c "from datetime import datetime, timedelta; from src.services.ticketmaster_client import fetch_events_ticketmaster as f; s=datetime.utcnow(); e=s+timedelta(days=2); d=f(city='Pittsburgh', start=s, end=e); print('ticketmaster events:', len(d.get('events', [])))"
```
Or via planner (with server running):
```powershell
uvicorn src.main:app --reload --port 8000
curl -X POST "http://localhost:8000/api/itinerary/options" -H "Content-Type: application/json" -d "{\
  \"city\": \"Pittsburgh, PA\", \
  \"start_date\": \"2025-09-12T09:00:00Z\", \
  \"end_date\": \"2025-09-13T20:00:00Z\" \
}" | python - <<PY
import sys, json; d=json.load(sys.stdin); print('used_sources:', d.get('used_sources'))
PY
```

2) Yelp Fusion (set YELP_API_KEY):
```powershell
$env:YELP_API_KEY="<YOUR_KEY>"
Invoke-RestMethod "http://localhost:8000/api/food/search?query=ramen&location=Pittsburgh,%20PA&limit=3" | ConvertTo-Json -Depth 5
```

Alternatively, run the pytest-based check (skips if no key):
```powershell
pytest -q -m external tests/test_yelp_client.py -q
```

You can also run all external tests together (keys set):
```powershell
pytest -q -m external -s
```

3) OpenWeather (set WEATHER_API_KEY) — check planner uses weather:
```powershell
$env:WEATHER_API_KEY="<YOUR_KEY>"
curl -X POST "http://localhost:8000/api/itinerary/options" -H "Content-Type: application/json" -d "{\
  \"city\": \"Pittsburgh, PA\", \
  \"start_date\": \"2025-09-12T09:00:00Z\", \
  \"end_date\": \"2025-09-13T20:00:00Z\" \
}" | python - <<PY
import sys, json; d=json.load(sys.stdin); print('used_sources:', d.get('used_sources'))
PY
```

4) Google Maps (set MAPS_API_KEY, MAPS_PROVIDER=google) — distance/time and filtering:
```powershell
$env:MAPS_PROVIDER="google"; $env:MAPS_API_KEY="<YOUR_KEY>"
curl -X POST "http://localhost:8000/api/itinerary/options" -H "Content-Type: application/json" -d "{\
  \"city\": \"Pittsburgh, PA\", \
  \"start_date\": \"2025-09-12T09:00:00Z\", \
  \"end_date\": \"2025-09-13T20:00:00Z\", \
  \"user_address\": \"5000 Forbes Ave, Pittsburgh, PA 15213\", \
  \"max_distance_miles\": 5 \
}" | python - <<PY
import sys, json; d=json.load(sys.stdin); opts=d.get('options',[]); acts=[a for day in (opts[0]['days'] if opts else []) for a in day['activities']]; print('sample distances:', [a.get('distance_miles') for a in acts])
PY
```

5) OpenAI (optional):
```powershell
$env:OPENAI_API_KEY="<YOUR_KEY>"
python -c "from src.services.classifier import classify_environment as c; print('gym indoor? ->', c('Indoor climbing gym event')); print('park outdoor? ->', c('Park festival with tents'))"
```

Optional pytest-based check (skips if no key):
```powershell
pytest -q -m external -s tests/test_classifier.py
```

If any integration is missing, the app gracefully degrades (e.g., haversine distances, minimal fallback itineraries), so you can proceed incrementally.


