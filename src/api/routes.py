"""
Title: API Routes
Team: Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks
Date: 2025-09-11
Summary: FastAPI routes for health and itinerary preview.
Disclaimer: This file includes AI-assisted content (GPT-5); reviewed and approved by the Purple Turtles team.
"""

from fastapi import APIRouter, HTTPException, Query
from datetime import datetime, timedelta
from ..models.itinerary import (
    ItineraryRequest,
    ItineraryResponse,
    ItineraryOptionsResponse,
)
from ..services.planner import build_itinerary, build_itinerary_options
from ..services.yelp_client import search_food
from ..services.visitpgh_scraper import fetch_this_week_events
from ..services.weather_client import fetch_forecast


router = APIRouter()


@router.get("/weather")
def get_weather():
    """
    Fetches weather forecast data for Pittsburgh (7-day + hourly)
    """
    data = fetch_forecast("Pittsburgh")
    return data


@router.get("/plan")
async def get_plan(start_date: str = Query(...)):
    """
    Generate a weekend itinerary for Pittsburgh.
    Frontend sends the start_date (YYYY-MM-DD), we build the itinerary.
    """
    try:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    except ValueError:
        return {"error": "Invalid date format. Use YYYY-MM-DD."}

    req = ItineraryRequest(
        city="Pittsburgh",
        start_date=start_dt,
        end_date=start_dt + timedelta(days=1),
        # preferences=ItineraryPreferences(
        #     interests=["food", "art", "music"], environment="either"
        # ),
    )

    itinerary = build_itinerary(req)

    # Transfer to json (readable by the frontend)
    result = {"start_date": start_date, "activities": []}

    for day in itinerary.days:
        for a in day.activities:
            time_info = (
                f"{a.start_time.strftime('%I:%M %p')}–{a.end_time.strftime('%I:%M %p')}"
                if a.start_time
                else ""
            )
            text = f"{time_info} {a.name} ({a.category})"
            if a.address:
                text += f" — {a.address}"
            result["activities"].append(text)

    return result
    
# @router.get("/plan")
# async def get_plan(start_date: str = Query(...)):
#     """
#     Generate a weekend itinerary for Pittsburgh.
#     Frontend sends the start_date (YYYY-MM-DD), we build the itinerary.
#     """
#     try:
#         start_dt = datetime.strptime(start_date, "%Y-%m-%d")
#     except ValueError:
#         return {"error": "Invalid date format. Use YYYY-MM-DD."}

#     req = ItineraryRequest(
#         city="Pittsburgh",
#         start_date=start_dt,
#         end_date=start_dt + timedelta(days=1),
#         # preferences=ItineraryPreferences(
#         #     interests=["food", "art", "music"], environment="either"
#         # ),
#     )

#     itinerary = build_itinerary(req)

    # # turn to json format (readable for frontend)
    # result = {"start_date": start_date, "activities": []}

    # for day in itinerary.days:
    #     for a in day.activities:
    #         time_info = (
    #             f"{a.start_time.strftime('%I:%M %p')}–{a.end_time.strftime('%I:%M %p')}"
    #             if a.start_time
    #             else ""
    #         )
    #         text = f"{time_info} {a.name} ({a.category})"
    #         if a.address:
    #             text += f" — {a.address}"
    #         result["activities"].append(text)

    # return result


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
