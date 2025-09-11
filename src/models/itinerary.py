"""
Title: Domain Models - Itinerary
Team: Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks
Date: 2025-09-11
Summary: Pydantic models for itinerary planning domain.
Disclaimer: This file includes AI-assisted content (GPT-5); reviewed and approved by the Purple Turtles team.
"""

from datetime import datetime, time
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


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


class DayPlan(BaseModel):
    date: datetime
    activities: List[Activity] = Field(default_factory=list)


class ItineraryRequest(BaseModel):
    city: str = Field("Pittsburgh, PA")
    start_date: datetime
    end_date: datetime
    preferences: Preference = Field(default_factory=Preference)


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


