# Weekender: Pittsburgh Plan-o-matic

**Team:** Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks  
**Date:** 2025-09-11  
**Setup Date:** 2025-09-13

## Overview
This is a complete full-stack web application for planning Pittsburgh weekend itineraries. The React frontend provides an interactive, user-friendly interface for discovering and planning Steel City adventures, while the FastAPI backend generates personalized itineraries. The app pulls event highlights from VisitPittsburgh (scraper) and Ticketmaster (API), food options from Yelp, and weather data from OpenWeather. It considers user's address, computes distances/times, filters by max distance, and sequences activities by proximity.

## Current State
✅ **PRODUCTION-READY FULL-STACK APPLICATION**
- **Frontend:** React with Vite on port 5000 (user-facing)
- **Backend:** FastAPI on port 8000 (API services)
- Python 3.11 and Node.js 20 environments installed
- All dependencies installed and configured
- Pittsburgh-themed responsive UI with Steel City colors
- Interactive features: date pickers, event browsing, itinerary planning
- CORS configured for cross-origin requests
- Environment-driven configuration for production deployment
- Both workflows running successfully with hot reload

## API Endpoints (Backend - Port 8000)
- `/api/health` - Health check
- `/api/events/this-week` - Pittsburgh events scraper
- `/api/itinerary` - Single itinerary generation
- `/api/itinerary/options` - Multiple itinerary options
- `/api/food/search` - Yelp food search (requires API key)
- `/docs` - Swagger UI documentation

## Frontend Features (Port 5000)
- **Home Page:** Pittsburgh-themed hero, live events preview, navigation
- **Itinerary Planner:** Interactive form with date picker, preferences, budget selection
- **Events Browser:** Filterable event cards with search and details
- **Results Display:** Beautiful timeline view of planned activities
- **Responsive Design:** Works perfectly on mobile, tablet, and desktop

## Recent Changes (2025-09-13)
- ✅ Set up complete React frontend with interactive features
- ✅ Configured backend on port 8000, frontend on port 5000
- ✅ Added proper CORS configuration with regex patterns
- ✅ Implemented environment-driven API configuration
- ✅ Fixed all production readiness issues
- ✅ Configured autoscale deployment for production
- ✅ Added comprehensive error handling and validation

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