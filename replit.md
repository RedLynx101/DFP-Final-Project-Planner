# Weekender: Pittsburgh Plan-o-matic

**Team:** Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks  
**Date:** 2025-09-11  
**Setup Date:** 2025-09-13

## Overview
This is a FastAPI backend application that generates Pittsburgh weekend itineraries. The app pulls event highlights from VisitPittsburgh (scraper) and Ticketmaster (API), food options from Yelp, and weather data from OpenWeather. It considers user's address, computes distances/times, filters by max distance, and sequences activities by proximity.

## Current State
✅ **FULLY CONFIGURED FOR REPLIT**
- Python 3.11 environment installed
- All dependencies installed from requirements.txt
- FastAPI backend running successfully on port 5000
- Workflow configured: `uvicorn src.main:app --host 0.0.0.0 --port 5000 --reload --log-level info`
- Deployment configured for autoscale mode
- All API endpoints tested and working:
  - `/api/health` - Health check
  - `/api/events/this-week` - Pittsburgh events scraper
  - `/api/itinerary` - Single itinerary generation
  - `/api/itinerary/options` - Multiple itinerary options
  - `/api/food/search` - Yelp food search (requires API key)
  - `/docs` - Swagger UI documentation

## Recent Changes (2025-09-13)
- Configured for Replit environment with port 5000 binding
- Set up FastAPI Backend workflow
- Configured deployment settings for production (autoscale)
- Verified all endpoints are functional
- Documentation accessible at `/docs`

## Project Architecture
```
src/
  main.py                 # FastAPI app entrypoint
  api/routes.py           # API routes
  core/config.py          # Settings via pydantic BaseSettings (.env supported)
  core/logging_config.py  # Logging configuration
  models/itinerary.py     # Pydantic models
  services/               # Business logic services
    planner.py            # Itinerary builder
    visitpgh_scraper.py   # VisitPittsburgh scraper
    ticketmaster_client.py# Ticketmaster API client
    yelp_client.py        # Yelp Fusion client
    maps_client.py        # Google Maps client
    weather_client.py     # OpenWeather client
    classifier.py         # Indoor/outdoor classification
```

## Configuration
- **Environment:** Uses .env file for API keys (optional)
- **Database:** SQLite default, configurable via DATABASE_URL
- **Port:** 5000 (Replit requirement)
- **Host:** 0.0.0.0 (allows external access)

## API Keys (Optional)
The app runs with fallbacks if these are not provided:
- `YELP_API_KEY` - Yelp Fusion API for food search
- `WEATHER_API_KEY` - OpenWeather API for weather data  
- `OPENAI_API_KEY` - OpenAI for classification refinement
- `TICKETMASTER_API_KEY` - Ticketmaster Discovery API
- `MAPS_API_KEY` - Google Maps for geocoding
- `MAPS_PROVIDER` - Set to "google" or "none"

## Testing
- Run tests: `pytest -q`
- External tests: `pytest -q -m external`
- Check API key status: `pytest -q -s tests/test_api_keys_status.py`