"""
Title: Domain Models - Itinerary
Team: Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks
Date: 2025-09-11
Summary: Pydantic models for itinerary planning domain.
Disclaimer: This file includes AI-assisted content (GPT-5); reviewed and approved by the Purple Turtles team.
"""

from datetime import datetime, time
from typing import List, Optional
from pydantic import BaseModel, Field


class Preference(BaseModel):
    budget_level: str = Field("medium", description="low|medium|high")
    interests: List[str] = Field(default_factory=lambda: ["food", "museums"])
    mobility: str = Field("walk", description="walk|transit|drive")


class Activity(BaseModel):
    name: str
    category: str
    address: Optional[str] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    cost_estimate: Optional[float] = None
    notes: Optional[str] = None


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


