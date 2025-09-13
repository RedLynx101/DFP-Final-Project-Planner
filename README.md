# Weekender: Pittsburgh Plan‑o‑matic

Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks

Date: 2025-09-11

Summary: FastAPI backend that generates Pittsburgh weekend itineraries. It pulls event highlights from VisitPittsburgh (scraper) and Ticketmaster (API), food options from Yelp (if API key provided), and weather from OpenWeather (if API key provided). It can consider a user's address, compute distances/times, filter by max distance, and sequence activities by proximity. If external services are unavailable, it falls back gracefully.

Disclaimer: This repository includes AI-assisted content (GPT-5); reviewed and approved by the Purple Turtles team.

## Quickstart

1) Python 3.11+ recommended.
2) Create and activate venv:
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```
3) Install deps:
```powershell
pip install -r requirements.txt
```
4) (Optional, recommended) Create `.env` and add API keys. Without keys, functionality is limited but the app still runs with fallbacks.
```env
# .env
APP_NAME=weekender
LOG_LEVEL=INFO

# External APIs (optional but recommended)
YELP_API_KEY=your_yelp_fusion_key
WEATHER_API_KEY=your_openweather_key
OPENAI_API_KEY=your_openai_key  # optional; classifier refinement
OPENAI_MODEL=gpt-5-nano         # default model used for OpenAI integrations
OPENAI_MAX_COMPLETION_TOKENS=500 # default tokens for OpenAI completions
TICKETMASTER_API_KEY=your_ticketmaster_key  # API-based events
MAPS_API_KEY=your_google_maps_key          # geocoding + distance matrix
MAPS_PROVIDER=google                       # or "none" for haversine fallback
```
5) Run the dev server (either):
```powershell
uvicorn --config config/uvicorn.ini src.main:app
# or
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Open http://localhost:8000/docs for Swagger UI (interactive testing).

More setup help: see `docs/ENV_SETUP.md` for a complete .env template and incremental testing steps (Ticketmaster, Yelp, Weather, Maps, OpenAI).

## API Endpoints

- `GET /api/health`: Basic health check.
- `POST /api/itinerary` → `ItineraryResponse`: Single best plan (uses the options builder; returns first option or a minimal fallback).
- `POST /api/itinerary/options` → `ItineraryOptionsResponse`: Up to three itinerary options based on events (VisitPgh + Ticketmaster), food (Yelp), weather, and distance from the user's address.
- `GET /api/food/search?query=ramen&location=Pittsburgh%2C%20PA&limit=5[&price=1,2]`: Yelp Fusion proxy. Requires `YELP_API_KEY`.
- `GET /api/events/this-week`: Scrapes VisitPittsburgh "This Week" page. No API key required; site structure changes may affect results.

Example request for `POST /api/itinerary` (with user address & max distance):
```bash
curl -X POST "http://localhost:8000/api/itinerary" \
  -H "Content-Type: application/json" \
  -d '{
    "city": "Pittsburgh, PA",
    "start_date": "2025-09-12T09:00:00Z",
    "end_date": "2025-09-14T18:00:00Z",
    "preferences": {"budget_level": "medium", "interests": ["food", "museums"], "mobility": "walk", "environment": "either"},
    "user_address": "5000 Forbes Ave, Pittsburgh, PA 15213",
    "max_distance_miles": 5
  }'
```

## Project Structure

```
src/
  main.py                 # FastAPI app entrypoint
  api/routes.py           # API routes (health, itinerary, search, events)
  core/config.py          # Settings via pydantic BaseSettings (.env supported)
  core/logging_config.py
  models/itinerary.py     # Pydantic models for request/response
  services/
    planner.py            # Builds itinerary options and single-plan fallback
    visitpgh_scraper.py   # Scrapes VisitPittsburgh events
    ticketmaster_client.py# Ticketmaster Discovery API client (requires API key)
    yelp_client.py        # Yelp Fusion client (requires API key)
    maps_client.py        # Geocode + distance matrix (Google), haversine fallback
    weather_client.py     # OpenWeather client + suitability scoring
tests/
  README.md               # Tests overview and how to run
  test_smoke.py           # Health + itinerary smoke
  test_planner_options.py # Itinerary options and single-plan compat
  test_scraper.py         # VisitPittsburgh scraper integration
  test_ticketmaster_client.py # Ticketmaster client tests
  test_yelp_client.py     # Yelp Fusion client tests
  test_maps_client.py     # Maps client (haversine + optional geocode)
  test_weather_client.py  # Weather utilities (suitability, mapping)
  test_classifier.py      # Heuristic classifier checks
config/
  uvicorn.ini
docs/
  ENV_SETUP.md            # .env template and step-by-step integration tests
assets/
notebooks/
```

## Development

- Run tests: `pytest -q`
- Lint (optional if you add): `ruff check .` and `black .`

Testing docs and structure: see `tests/README.md`.
By default, tests marked `@pytest.mark.external` are excluded (see `pytest.ini`).
Run external tests with:
```powershell
pytest -q -m external
```

Key status report (to see which integrations are active). Use `-s` to show prints:
```powershell
pytest -q -s tests/test_api_keys_status.py
```

## Environment & Keys

Create a `.env` (optional) to enable external integrations. Keep real secrets out of version control. Common variables:
- `YELP_API_KEY` (Yelp Fusion API) — enables `/api/food/search` and richer food picks in itineraries
- `WEATHER_API_KEY` (OpenWeather) — enables weather-aware planning
- `OPENAI_API_KEY` (optional) — may refine indoor/outdoor classification; heuristics are used otherwise
- `TICKETMASTER_API_KEY` — enables Ticketmaster events (API-based source)
- `MAPS_API_KEY`, `MAPS_PROVIDER` — enables geocoding + travel distance/time (Google)
- `APP_NAME`, `LOG_LEVEL` — general app config

Behavior without keys:
- The app still starts. VisitPittsburgh scraping is attempted for events. Yelp, Ticketmaster, Weather, and Maps features are skipped if keys are missing; the planner returns what it can and may provide a minimal fallback itinerary.

## License

Academic project for CMU course. Team: Purple Turtles.

---

What it does right now:
- Generates up to three itinerary options considering events (VisitPittsburgh + Ticketmaster), food (Yelp), weather (OpenWeather), and distance from a user-provided address (Google Maps if configured, haversine fallback). Applies a max-distance filter and prefers closer items when sequencing. Falls back if sources are unavailable.


