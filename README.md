# Weekender: Pittsburgh Plan‑o‑matic

Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks

Date: 2025-09-11

Summary: A planning tool to generate personalized weekend itineraries in Pittsburgh based on user preferences, events, weather, transit and budget. This repo contains a FastAPI backend scaffolding, configuration, and testing framework to iterate quickly toward the CMU Python Final Project.

Disclaimer: This repository includes AI-assisted content (GPT-5); reviewed and approved by the Purple Turtles team.

## Quickstart

1) Python 3.11+ recommended.
2) Create and activate venv:
```powershell
python -m venv .venv
.venv\\Scripts\\Activate.ps1
```
3) Install deps:
```powershell
pip install -r requirements.txt
```
4) Copy env and set keys:
```powershell
cp .env.example .env
```
5) Run dev server:
```powershell
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Open http://localhost:8000/docs for Swagger UI.

## Project Structure

```
src/
  main.py              # FastAPI app factory and startup
  api/routes.py        # API router registration
  core/config.py       # Settings via pydantic BaseSettings
  core/logging_config.py
  services/planner.py  # Itinerary planning service (stub)
  models/itinerary.py  # Pydantic models for domain
tests/
  test_smoke.py        # Basic health test
config/
  uvicorn.ini
docs/                  # Additional docs, design notes
assets/                # Static assets
notebooks/             # Exploration notebooks
```

## Development

- Run tests: `pytest -q`
- Lint (optional if you add): `ruff check .` and `black .`

## Environment & Keys

Configure `.env` using `.env.example`. Keep real secrets out of version control. Placeholders are provided for:
- OPENAI_API_KEY
- MAPS_API_KEY (e.g., Google, Mapbox, or OpenRouteService)
- WEATHER_API_KEY (e.g., OpenWeather)
- EVENTS_API_KEY (e.g., Ticketmaster, Eventbrite)

## Rubric & Proposal

- See `final_project_rubric.docx` and proposal PDF in the repo root.

## License

Academic project for CMU course. Team: Purple Turtles.


