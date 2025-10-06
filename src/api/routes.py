"""
Title: API Routes
Team: Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks
Date: 2025-09-11
Summary: FastAPI routes for health and itinerary preview.
Disclaimer: This file includes AI-assisted content (GPT-5); reviewed and approved by the Purple Turtles team.
"""

from fastapi import APIRouter, HTTPException, Query
from fastapi.encoders import jsonable_encoder
import logging
import traceback
from datetime import datetime, timedelta
from types import SimpleNamespace
from src.models.itinerary import (
    ItineraryRequest,
    ItineraryResponse,
    ItineraryOptionsResponse,
    Preference,
)
from src.services.planner import build_itinerary, build_itinerary_options
from src.services.yelp_client import search_food
from src.services.visitpgh_scraper import fetch_this_week_events
from src.services.weather_client import fetch_forecast


router = APIRouter()
print("🚀 routes_planner loaded successfully!")


@router.get("/weather")
async def get_weather():
    """
    Fetches weather forecast data for Pittsburgh (7-day + hourly)
    """
    print("📅 get_weather() called successfully")

    data = fetch_forecast("Pittsburgh")
    return data


@router.get("/plan")
async def get_plan(
    start_date: str = Query(...),
    address: str = Query("Pittsburgh, PA"),
    days: int = Query(2),
):
    """
    Generate itinerary for given date and location.
    """
    print("📅 get_plan() called successfully")

    try:
        # Convert date
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = start_dt + timedelta(days=days - 1)
        print(f"Start: {start_dt}, End: {end_dt}, Address: {address}")

        pref = Preference(
            budget_level="medium",
            interests=["food", "museums", "art"],
            mobility="walk",
            environment="either",
        )

        request_obj = ItineraryRequest(
            city=address,
            start_date=start_dt,
            end_date=end_dt,
            preferences=pref,
            user_address=address,
            max_distance_miles=5.0,
        )

        itinerary = build_itinerary(request_obj)

        print("✅ Itinerary built successfully!")
        return jsonable_encoder({"start_date": start_date, "activities": itinerary})

    except Exception as e:
        print("❌ ERROR in get_plan():", e)
        traceback.print_exc()
        return {"error": f"Failed to build itinerary: {e}"}


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.post(
    "/itinerary",
    response_model=ItineraryResponse,
    summary="Build a single itinerary (defaults to upcoming weekend at CMU)",
)
def create_itinerary(payload: ItineraryRequest) -> ItineraryResponse:
    return build_itinerary(payload)


@router.get("/food/search")
def food_search(
    query: str,
    location: str = "Pittsburgh, PA",
    limit: int = 5,
    price: str | None = None,
) -> dict:
    try:
        return search_food(query=query, location=location, limit=limit, price=price)
    except Exception as exc:  # pragma: no cover - network failures translate to 502
        raise HTTPException(status_code=502, detail=str(exc))


@router.get("/events/this-week")
def events_this_week() -> dict:
    try:
        return fetch_this_week_events()
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=502, detail=str(exc))


@router.post(
    "/itinerary/options",
    response_model=ItineraryOptionsResponse,
    summary="Build multiple itinerary options (diversified; defaults prefilled)",
)
def create_itinerary_options(payload: ItineraryRequest) -> ItineraryOptionsResponse:
    try:
        return build_itinerary_options(payload)
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=str(exc))
