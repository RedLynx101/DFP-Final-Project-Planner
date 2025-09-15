# Weekender: Pittsburgh Plan‑o‑matic (Submission-Ready)

Team: Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks

Date: 2025-09-15

Summary: FastAPI backend that generates Pittsburgh weekend itineraries with data from VisitPittsburgh (scraper), Ticketmaster (API), Yelp (API), and OpenWeather (API). Works without keys with graceful fallbacks.

Disclaimer: This repository includes AI-assisted content (GPT-5); reviewed and approved by the Purple Turtles team.

## CMU IDs (for grading)

- Noah Hicks — nhicks 
- Aadya Agarwal — aadyaaga
- Emma Peng — yepeng
- Gwen Li — wendyl2

## Install

1) Python 3.11+ recommended.
2) Create and activate venv:
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```
3) Install packages (pick one):
```powershell
pip install -r requirements.txt
```

Manual install (alternative):
```powershell
pip install fastapi==0.112.2
pip install "uvicorn[standard]==0.30.6"
pip install pydantic==2.9.2
pip install pydantic-settings==2.6.1
pip install python-dotenv==1.0.1
pip install httpx==0.27.2
pip install anyio==4.4.0
pip install beautifulsoup4==4.12.3
pip install lxml==5.3.0   # optional; falls back to html.parser if absent
pip install python-dateutil==2.9.0.post0
pip install openai==1.51.2
```

## Configure (optional)

Create a `.env` in the repo root for API keys. The app runs without keys, but features are limited.
```env
# App
APP_NAME=weekender
LOG_LEVEL=INFO

# External APIs (optional)
YELP_API_KEY=
WEATHER_API_KEY=
TICKETMASTER_API_KEY=
MAPS_PROVIDER=google
MAPS_API_KEY=
# Optional OpenAI (classifier refinement)
OPENAI_API_KEY=
OPENAI_MODEL=gpt-5-nano
OPENAI_MAX_COMPLETION_TOKENS=500
```

## Run

From the repo root (flat layout):
```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
Open `http://localhost:8000/docs` for Swagger UI.

## API (frontend usage)

- GET `/api/health` → `{ "status": "ok" }`
- POST `/api/itinerary` → `ItineraryResponse`
- POST `/api/itinerary/options` → `ItineraryOptionsResponse`
- GET `/api/food/search?query=ramen&location=Pittsburgh,%20PA&limit=5[&price=1,2]` → Yelp proxy (requires `YELP_API_KEY`)
- GET `/api/events/this-week` → VisitPittsburgh scraper

Example:
```bash
curl -X POST "http://localhost:8000/api/itinerary" \
  -H "Content-Type: application/json" \
  -d '{
    "city": "Pittsburgh, PA",
    "user_address": "Hamburg Hall, 4800 Forbes Ave, Pittsburgh, PA 15213",
    "max_distance_miles": 5
  }'
```

## Files (flat)

```
main.py              # FastAPI app entry
routes.py            # API routes
config.py            # Settings (.env supported)
logging_config.py    # Logging setup
itinerary.py         # Pydantic models
planner.py           # Itinerary builder
visitpgh_scraper.py  # VisitPittsburgh scraper
ticketmaster_client.py
yelp_client.py
maps_client.py
weather_client.py
requirements.txt
README.md
.env (optional)
```

## Notes for graders

- The app runs without any API keys (reduced features; graceful fallbacks).
- All code lives in the repo root for easy review.
- Title, team, authors, summary, and AI disclaimer are included in each module header.



