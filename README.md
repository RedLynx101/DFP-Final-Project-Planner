# Weekender: Pittsburgh Plan‑o‑matic

Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks

Date: 2025-09-11

Summary: FastAPI backend that generates Pittsburgh weekend itineraries. It pulls event highlights from VisitPittsburgh, food options from Yelp (if API key provided), and weather from OpenWeather (if API key provided). It returns one or multiple itinerary options and gracefully falls back if external services are unavailable.

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
OPENAI_API_KEY=your_openai_key  # optional; used for classifier refinement
```
5) Run the dev server (either):
```powershell
uvicorn --config config/uvicorn.ini src.main:app
# or
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Open http://localhost:8000/docs for Swagger UI (interactive testing).

## API Endpoints

- `GET /api/health`: Basic health check.
- `POST /api/itinerary` → `ItineraryResponse`: Single best plan (uses the options builder under the hood; returns the first option or a minimal fallback if sources fail).
- `POST /api/itinerary/options` → `ItineraryOptionsResponse`: Up to three itinerary options based on events, food, and weather.
- `GET /api/food/search?query=ramen&location=Pittsburgh%2C%20PA&limit=5[&price=1,2]`: Yelp Fusion proxy. Requires `YELP_API_KEY`.
- `GET /api/events/this-week`: Scrapes VisitPittsburgh "This Week" page. No API key required; site structure changes may affect results.

Example request for `POST /api/itinerary`:
```bash
curl -X POST "http://localhost:8000/api/itinerary" \
  -H "Content-Type: application/json" \
  -d '{
    "city": "Pittsburgh, PA",
    "start_date": "2025-09-12T09:00:00Z",
    "end_date": "2025-09-14T18:00:00Z",
    "preferences": {"budget_level": "medium", "interests": ["food", "museums"], "mobility": "walk", "environment": "either"}
  }'
```

## Project Structure

```
src/
  main.py               # FastAPI app entrypoint
  api/routes.py         # API routes (health, itinerary, search, events)
  core/config.py        # Settings via pydantic BaseSettings (.env supported)
  core/logging_config.py
  models/itinerary.py   # Pydantic models for request/response
  services/
    planner.py          # Builds itinerary options and single-plan fallback
    visitpgh_scraper.py # Scrapes VisitPittsburgh events
    yelp_client.py      # Yelp Fusion client (requires API key)
    weather_client.py   # OpenWeather client + suitability scoring
tests/
  test_smoke.py
  test_planner_options.py
config/
  uvicorn.ini
docs/
assets/
notebooks/
```

## Development

- Run tests: `pytest -q`
- Lint (optional if you add): `ruff check .` and `black .`

## Environment & Keys

Create a `.env` (optional) to enable external integrations. Keep real secrets out of version control. Common variables:
- `YELP_API_KEY` (Yelp Fusion API) — enables `/api/food/search` and richer food picks in itineraries
- `WEATHER_API_KEY` (OpenWeather) — enables weather-aware planning
- `OPENAI_API_KEY` (optional) — may refine indoor/outdoor classification; heuristics are used otherwise
- `APP_NAME`, `LOG_LEVEL` — general app config

Behavior without keys:
- The app still starts. VisitPittsburgh scraping is attempted for events. Yelp and weather calls are skipped; planner returns what it can and will provide a minimal fallback plan if sources are unavailable.

## Rubric & Proposal

- See `final_project_rubric.docx` and proposal PDF in the repo root.

## License

Academic project for CMU course. Team: Purple Turtles.

---

What it does right now:
- Exposes a FastAPI service that can generate up to three itinerary options for a given date range in Pittsburgh, mixing event picks (VisitPittsburgh), food picks (Yelp, if key), and weather suitability (OpenWeather, if key). If external sources fail or are not configured, it returns a minimal, sensible fallback itinerary so tests and demos still succeed.


