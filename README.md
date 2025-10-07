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

### Option 1: Interactive Console UI (Recommended for Quick Start) 🎨

The easiest way to use Weekender is through the interactive menu system:

```powershell
python cli.py
```

This launches a beautiful ASCII-art console interface with:
- 🎭 **Animated intro** with team credits
- 📋 **Interactive menu** with 7 options:
  1. Build Single Weekend Itinerary
  2. Build Multiple Itinerary Options
  3. Search Food (Yelp)
  4. View This Week's Events
  5. Build Itinerary & Export JSON
  6. Test API Keys (Diagnostics)
  7. Exit
- 🔑 **API Status Display**: Shows "X/5 keys configured" at menu bottom
- ✨ **Loading animations** and pretty-formatted output
- 🔄 **Automatic menu loop** after each operation
- ✅ **Input validation** with helpful defaults

No command-line arguments needed—just run and follow the prompts!

#### API Key Diagnostics

The CLI includes a comprehensive API testing tool (Option 6) that validates all configured API keys:

- **OpenAI**: Tests chat completion endpoint with configured model
- **Google Maps**: Tests geocoding service with Pittsburgh coordinates  
- **Weather (OpenWeather)**: Tests forecast retrieval for Pittsburgh
- **Yelp**: Tests restaurant search functionality
- **Ticketmaster**: Tests event discovery API

Each test displays:
- ✅ **WORKING**: API key configured and functioning properly
- ❌ **FAILED**: API key configured but calls are failing (shows error details)
- ⚠️ **NOT CONFIGURED**: No API key set in environment

Results include specific details like response data or error messages to help troubleshoot issues. The main menu also shows a quick status summary (e.g., "🔑 API Status: 4/5 keys configured").

### Option 2: Web API with Swagger UI

For programmatic access or if you're building a frontend:

```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Then open `http://localhost:8000/docs` for interactive Swagger UI.

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
cli.py                                # Interactive console UI (animated menu system)
main.py                               # FastAPI app entry
routes.py                             # API routes: /api/health, /api/itinerary, /api/itinerary/options, /api/food/search, /api/events/this-week
config.py                             # Settings (.env supported) via pydantic BaseSettings
logging_config.py                     # Structured logging setup
itinerary.py                          # Pydantic domain models/schemas
planner.py                            # Itinerary builder core logic (events, food, weather, maps)
visitpgh_scraper.py                   # VisitPittsburgh 'This Week' scraper
ticketmaster_client.py                # Ticketmaster Discovery API client
yelp_client.py                        # Yelp Fusion API client for food search
maps_client.py                        # Geocoding + distance; Google or haversine fallback
weather_client.py                     # OpenWeather forecast + outdoor suitability mapping
classifier.py                         # Indoor/Outdoor classifier (heuristic + optional OpenAI)
requirements.txt                      # Python dependencies
README.md                             # This documentation                         
.env (optional)                       # Local environment configuration (not committed)
```

## Notes for graders

- **Quickest way to demo:** Just run `python cli.py` and explore the interactive menu! 🎨
- **API Key Testing:** Use Option 6 in the CLI to see which APIs are configured and working
- The app runs without any API keys (reduced features; graceful fallbacks).
- All code lives in the repo root for easy review.
- Title, team, authors, summary, and AI disclaimer are included in each module header.
- The console UI features ASCII art, loading animations, and a full menu-driven experience.



