"""
Title: Domain Models - Itinerary
Team: Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks
Date: 2025-09-15
Summary: Pydantic models for itinerary planning domain.
Disclaimer: This file includes AI-assisted content (GPT-5); reviewed and approved by the Purple Turtles team.
"""

from datetime import datetime, time, timedelta
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, ConfigDict


def _next_weekend_start() -> datetime:
    """Compute the upcoming Saturday at 09:00 local time.

    If today is Saturday but past 09:00, keep today; otherwise next Saturday.
    """
    now = datetime.now()
    # Monday=0 ... Sunday=6; Saturday=5
    days_until_sat = (5 - now.weekday()) % 7
    sat = now + timedelta(days=days_until_sat)
    start = sat.replace(hour=9, minute=0, second=0, microsecond=0)
    if days_until_sat == 0 and now < start:
        # It's Saturday before 09:00 → use today 09:00
        return start
    if days_until_sat == 0 and now >= start:
        # It's Saturday after 09:00 → keep today to include the rest of day
        return start
    return start


def _next_weekend_end() -> datetime:
    """Compute the upcoming Sunday at 21:00 local time based on next weekend start."""
    sat_start = _next_weekend_start()
    sun_end = (sat_start + timedelta(days=1)).replace(hour=21, minute=0, second=0, microsecond=0)
    return sun_end


class Preference(BaseModel):
    budget_level: str = Field("medium", description="low|medium|high")
    interests: List[str] = Field(default_factory=lambda: ["food", "museums"])
    mobility: str = Field("walk", description="walk|transit|drive")
    environment: str = Field(
        "either", description="indoor|outdoor|either"
    )


class Activity(BaseModel):
    name: str
    category: str
    address: Optional[str] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    cost_estimate: Optional[float] = None
    notes: Optional[str] = None
    external_url: Optional[str] = None
    source: Optional[str] = Field(None, description="source identifier e.g. visitpgh|yelp")
    environment: Optional[str] = Field(None, description="indoor|outdoor|unknown")
    coordinates: Optional[Dict[str, float]] = Field(
        None, description="Geographic coordinates {lat, lon} if known"
    )
    distance_miles: Optional[float] = Field(
        None, description="Distance from user's origin in miles if origin provided"
    )
    travel_time_minutes: Optional[int] = Field(
        None, description="Estimated travel time from previous stop or origin"
    )


class DayPlan(BaseModel):
    date: datetime
    activities: List[Activity] = Field(default_factory=list)


class ItineraryRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "city": "Pittsburgh, PA",
                "start_date": _next_weekend_start().isoformat(),
                "end_date": _next_weekend_end().isoformat(),
                "preferences": {"budget_level": "medium", "interests": ["food", "museums"], "mobility": "walk", "environment": "either"},
                "user_address": "Hamburg Hall, 4800 Forbes Ave, Pittsburgh, PA 15213",
                "max_distance_miles": 5,
            }
        }
    )
    city: str = Field("Pittsburgh, PA")
    start_date: datetime = Field(default_factory=_next_weekend_start, description="Start datetime; defaults to upcoming Saturday 09:00")
    end_date: datetime = Field(default_factory=_next_weekend_end, description="End datetime; defaults to upcoming Sunday 21:00")
    preferences: Preference = Field(default_factory=Preference)
    user_address: Optional[str] = Field(
        "Hamburg Hall, 4800 Forbes Ave, Pittsburgh, PA 15213",
        description="User origin street address for distance calculations (default: Hamburg Hall, CMU)",
    )
    max_distance_miles: Optional[float] = Field(
        5, description="Maximum distance from origin in miles for included activities (default: 5)"
    )


class ItineraryResponse(BaseModel):
    title: str
    days: List[DayPlan]
    summary: Optional[str] = None
    warnings: List[str] = Field(default_factory=list)
    sources: Dict[str, int] = Field(default_factory=dict, description="counts of items by source")


class EventItem(BaseModel):
    title: str
    details: Optional[str] = None
    url: Optional[str] = None
    date_hint: Optional[str] = Field(
        None, description="free-text date/day info scraped from the page"
    )
    environment: Optional[str] = Field(None, description="indoor|outdoor|unknown")


class ItineraryOptionsResponse(BaseModel):
    options: List[ItineraryResponse]
    warnings: List[str] = Field(default_factory=list)
    used_sources: Dict[str, int] = Field(default_factory=dict)


class YelpSearchResponse(BaseModel):
    query: str
    location: str
    results: List[dict]


