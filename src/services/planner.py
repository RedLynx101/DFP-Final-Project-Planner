"""
Title: Planner Service
Team: Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks
Date: 2025-09-11
Summary: Stub itinerary planner service. Integrations to maps, events, and weather will be added.
Disclaimer: This file includes AI-assisted content (GPT-5); reviewed and approved by the Purple Turtles team.
"""

from datetime import timedelta
from typing import List
from ..models.itinerary import (
    ItineraryRequest,
    ItineraryResponse,
    DayPlan,
    Activity,
)


def build_itinerary(request: ItineraryRequest) -> ItineraryResponse:
    # Placeholder logic: create simple morning/afternoon/evening blocks
    days: List[DayPlan] = []
    current = request.start_date
    while current.date() <= request.end_date.date():
        day = DayPlan(
            date=current,
            activities=[
                Activity(
                    name="Breakfast at local cafe",
                    category="food",
                    notes="Placeholder recommendation",
                ),
                Activity(
                    name="Museum visit",
                    category="museums",
                    notes="Carnegie or Warhol",
                ),
                Activity(
                    name="Evening walk by the Point",
                    category="outdoors",
                    notes="Point State Park",
                ),
            ],
        )
        days.append(day)
        current = current + timedelta(days=1)

    return ItineraryResponse(
        title=f"Weekend in {request.city}",
        days=days,
        summary="Initial draft itinerary. Real data integrations pending.",
    )


