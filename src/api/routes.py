"""
Title: API Routes
Team: Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks
Date: 2025-09-11
Summary: FastAPI routes for health and itinerary preview.
Disclaimer: This file includes AI-assisted content (GPT-5); reviewed and approved by the Purple Turtles team.
"""

from fastapi import APIRouter
from ..models.itinerary import ItineraryRequest, ItineraryResponse
from ..services.planner import build_itinerary


router = APIRouter()


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.post("/itinerary", response_model=ItineraryResponse)
def create_itinerary(payload: ItineraryRequest) -> ItineraryResponse:
    return build_itinerary(payload)


