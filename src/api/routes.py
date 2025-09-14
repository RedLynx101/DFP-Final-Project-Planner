"""
Title: API Routes
Team: Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks
Date: 2025-09-11
Summary: FastAPI routes for health and itinerary preview.
Disclaimer: This file includes AI-assisted content (GPT-5); reviewed and approved by the Purple Turtles team.
"""

from fastapi import APIRouter, HTTPException
from ..models.itinerary import ItineraryRequest, ItineraryResponse, ItineraryOptionsResponse
from ..services.planner import build_itinerary, build_itinerary_options
from ..services.yelp_client import search_food
from ..services.visitpgh_scraper import fetch_this_week_events


router = APIRouter()


@router.get("/health")
def health() -> dict:
    """Enhanced health check endpoint for deployment health checks"""
    return {
        "status": "healthy",
        "service": "Pittsburgh Weekend Planner API",
        "version": "1.0.0",
        "timestamp": "2025-09-14T04:10:45Z"
    }


@router.post(
    "/itinerary",
    response_model=ItineraryResponse,
    summary="Build a single itinerary (defaults to upcoming weekend at CMU)",
)
def create_itinerary(payload: ItineraryRequest) -> ItineraryResponse:
    return build_itinerary(payload)


@router.get("/food/search")
def food_search(query: str, location: str = "Pittsburgh, PA", limit: int = 5, price: str | None = None) -> dict:
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

