"""
Title: Planner Service
Team: Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks
Date: 2025-09-11
Summary: Builds itineraries from real data sources (VisitPgh, Yelp, Weather) with fallbacks.
Disclaimer: This file includes AI-assisted content (GPT-5); reviewed and approved by the Purple Turtles team.
"""

from __future__ import annotations

from datetime import datetime, timedelta
import re
from typing import Any, Dict, Iterable, List, Optional, Tuple

from dateutil import parser as date_parser

from ..models.itinerary import (
    ItineraryRequest,
    ItineraryResponse,
    ItineraryOptionsResponse,
    DayPlan,
    Activity,
)
from .visitpgh_scraper import fetch_this_week_events
from .yelp_client import search_food
from .classifier import classify_environment
from .weather_client import fetch_forecast, map_forecast_to_days
from .maps_client import geocode_address, distance_matrix_miles
from .ticketmaster_client import fetch_events_ticketmaster


WEEKDAY_NAMES = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
]


def _daterange(start: datetime, end: datetime) -> Iterable[datetime]:
    cur = start
    while cur.date() <= end.date():
        yield cur
        cur = cur + timedelta(days=1)


def _parse_day_from_text(text: str) -> Optional[str]:
    lowered = text.lower()
    for name in WEEKDAY_NAMES:
        if name in lowered:
            return name
    # Try date like Sep 14, 2025 -> weekday
    try:
        dt = date_parser.parse(text, fuzzy=True, default=datetime(2000, 1, 1))
        return WEEKDAY_NAMES[dt.weekday()]
    except Exception:
        return None


def _weekday_from_iso_datetime(dt_str: Optional[str]) -> Optional[str]:
    if not dt_str:
        return None
    try:
        dt = date_parser.parse(dt_str, fuzzy=True)
        return WEEKDAY_NAMES[dt.weekday()]
    except Exception:
        return None


def _pittsburgh_coords() -> Dict[str, float]:
    return {"lat": 40.4406, "lon": -79.9959}


def _pick_non_overlapping_blocks(
    day: datetime,
    candidates: List[Dict[str, Any]],
    env_preference: str,
    weather_day_info: Optional[Dict[str, Any]],
) -> List[Activity]:
    blocks: List[Tuple[str, Tuple[int, int]]] = [
        ("morning", (9, 11)),
        ("afternoon", (13, 15)),
        ("evening", (18, 21)),
    ]

    suitability = weather_day_info.get("suitability") if weather_day_info else None
    chosen: List[Activity] = []

    # Simple strategy: pick one food for morning/evening, one event for afternoon
    def match_env(env: Optional[str]) -> bool:
        if env_preference == "either" or env_preference is None:
            return True
        if env is None or env == "unknown":
            return True  # allow unknowns; filtered later by weather when outdoor is poor
        return env == env_preference

    # Partition candidates
    food = [c for c in candidates if c.get("category") == "food" and match_env(c.get("environment"))]
    events = [c for c in candidates if c.get("category") != "food" and match_env(c.get("environment"))]

    # Weather-based filtering for outdoor preference
    if env_preference == "outdoor" and suitability is not None and suitability < 0.4:
        # If outdoor is poor, prefer indoor events and record via notes
        events = [c for c in candidates if (c.get("environment") == "indoor" or c.get("environment") is None)]

    def to_activity(item: Dict[str, Any], start_h: int, end_h: int) -> Activity:
        return Activity(
            name=item.get("name") or item.get("title") or "Activity",
            category=item.get("category") or item.get("type") or "activity",
            address=item.get("address"),
            start_time=datetime(day.year, day.month, day.day, start_h, 0).time(),
            end_time=datetime(day.year, day.month, day.day, end_h, 0).time(),
            notes=item.get("notes"),
            external_url=item.get("url"),
            source=item.get("source"),
            environment=item.get("environment"),
        )

    # Morning: breakfast
    if food:
        chosen.append(to_activity(food[0], *blocks[0][1]))
    # Afternoon: event
    if events:
        chosen.append(to_activity(events[0], *blocks[1][1]))
    # Evening: dinner
    if len(food) > 1:
        chosen.append(to_activity(food[1], *blocks[2][1]))
    elif food:
        # reuse breakfast place for dinner only if no alternative
        chosen.append(to_activity(food[0], *blocks[2][1]))

    return chosen


def _collect_candidates(
    city: str,
    interests: List[str],
    env_pref: str,
) -> Tuple[List[Dict[str, Any]], List[str], Dict[str, int]]:
    warnings: List[str] = []
    sources: Dict[str, int] = {}
    candidates: List[Dict[str, Any]] = []

    # VisitPgh events (web-scraped)
    try:
        events_payload = fetch_this_week_events()
        for e in events_payload.get("events", []):
            title = e.get("title") or ""
            details = e.get("details") or ""
            url = e.get("url")
            env = classify_environment(f"{title} {details}")
            day_name = _parse_day_from_text(f"{title} {details}")
            candidates.append(
                {
                    "title": title,
                    "category": "event",
                    "type": "event",
                    "notes": details,
                    "url": url,
                    "source": "visitpgh",
                    "environment": env,
                    "day_name": day_name,
                }
            )
        sources["visitpgh"] = len(events_payload.get("events", []))
    except Exception as exc:
        warnings.append(f"visitpgh_unavailable: {exc}")

    # Yelp food
    try:
        breakfast = search_food(query="breakfast", location=city, limit=5)
        dinner = search_food(query="dinner", location=city, limit=5)
        sources["yelp"] = len(breakfast.get("results", [])) + len(dinner.get("results", []))
        for b in breakfast.get("results", [])[:3]:
            candidates.append(
                {
                    "name": b.get("name"),
                    "category": "food",
                    "address": b.get("location"),
                    "url": b.get("url"),
                    "source": "yelp",
                    "environment": "indoor",  # default assumption
                }
            )
        for d in dinner.get("results", [])[:3]:
            candidates.append(
                {
                    "name": d.get("name"),
                    "category": "food",
                    "address": d.get("location"),
                    "url": d.get("url"),
                    "source": "yelp",
                    "environment": "indoor",
                }
            )
    except Exception as exc:
        warnings.append(f"yelp_unavailable: {exc}")

    # Ticketmaster events (API)
    try:
        # For MVP, query broadly for date range around now; refined windowing will happen per request
        tm_payload = fetch_events_ticketmaster(city="Pittsburgh")
        for e in tm_payload.get("events", []):
            title = e.get("title") or ""
            details = e.get("details") or ""
            url = e.get("url")
            env = classify_environment(f"{title} {details}")
            day_name = _weekday_from_iso_datetime(e.get("start_datetime"))
            candidates.append(
                {
                    "title": title,
                    "category": "event",
                    "type": "event",
                    "notes": details,
                    "url": url,
                    "source": "ticketmaster",
                    "environment": env,
                    "day_name": day_name,
                    "coordinates": e.get("coordinates"),
                }
            )
        sources["ticketmaster"] = len(tm_payload.get("events", []))
    except Exception as exc:
        warnings.append(f"ticketmaster_unavailable: {exc}")

    # Filter by interests loosely if provided (keep broad for MVP)
    if interests:
        keep: List[Dict[str, Any]] = []
        for c in candidates:
            if c.get("category") == "food":
                keep.append(c)
                continue
            text = (c.get("title") or "") + " " + (c.get("notes") or "")
            if any(i.lower() in text.lower() for i in interests):
                keep.append(c)
            else:
                # retain some events even if not matched to keep options
                keep.append(c)
        candidates = keep

    return candidates, warnings, sources


def build_itinerary_options(request: ItineraryRequest) -> ItineraryOptionsResponse:
    warnings: List[str] = []
    used_sources: Dict[str, int] = {}

    # Weather
    daily_weather: Dict[str, Dict[str, Any]] = {}
    try:
        forecast = fetch_forecast(request.city)
        daily_weather = map_forecast_to_days(forecast)
        used_sources["openweather"] = len(daily_weather)
    except Exception as exc:
        warnings.append(f"weather_unavailable: {exc}")

    candidates, w2, s2 = _collect_candidates(
        city=request.city,
        interests=request.preferences.interests,
        env_pref=request.preferences.environment,
    )
    warnings.extend(w2)
    for k, v in s2.items():
        used_sources[k] = used_sources.get(k, 0) + v

    # Geocode user origin if provided
    origin_coords: Optional[Dict[str, float]] = None
    if request.user_address:
        origin_coords = geocode_address(request.user_address)
        if origin_coords is None:
            # Fallback to Pittsburgh center to avoid breakage
            origin_coords = _pittsburgh_coords()

    # Attach distances from origin when possible and filter by max distance if requested
    if origin_coords is not None:
        dests = [c.get("coordinates") for c in candidates]
        # For items without coords, attempt naive geocode by address once
        for c in candidates:
            if not c.get("coordinates") and c.get("address"):
                gc = geocode_address(c["address"])  # may be None
                if gc:
                    c["coordinates"] = gc
        destinations = [c.get("coordinates") or origin_coords for c in candidates]
        matrix = distance_matrix_miles([origin_coords], destinations)
        if matrix:
            row0 = matrix[0]
            for idx, c in enumerate(candidates):
                dm = row0[idx]
                c["distance_miles"] = dm.get("distance_miles")
                c["duration_minutes"] = dm.get("duration_minutes")

        if request.max_distance_miles is not None:
            def within_limit(item: Dict[str, Any]) -> bool:
                dist = item.get("distance_miles")
                if dist is None:
                    return True  # keep unknowns to avoid over-filtering
                return dist <= request.max_distance_miles

            candidates = [c for c in candidates if within_limit(c)]

    # Build up to 3 options by selecting different events per day
    options: List[ItineraryResponse] = []
    day_dates = list(_daterange(request.start_date, request.end_date))
    day_names = [WEEKDAY_NAMES[d.weekday()] for d in day_dates]

    if not day_dates:
        return ItineraryOptionsResponse(options=[], warnings=warnings, used_sources=used_sources)

    # Group events by day name
    events_by_day: Dict[str, List[Dict[str, Any]]] = {dn: [] for dn in day_names}
    for c in candidates:
        dn = c.get("day_name")
        if dn in events_by_day:
            events_by_day[dn].append(c)
        elif c.get("category") != "food":
            # Unknown day: allow as fallback for any day
            events_by_day.setdefault("unknown", []).append(c)

    # For each option, pick a different featured event when possible
    for opt_idx in range(3):
        days: List[DayPlan] = []
        used_titles: set[str] = set()
        for day_dt in day_dates:
            dn = WEEKDAY_NAMES[day_dt.weekday()]
            day_weather = daily_weather.get(day_dt.date().isoformat())

            # Candidate pool for this day
            day_events = [e for e in events_by_day.get(dn, []) if e.get("title") not in used_titles]
            if not day_events:
                day_events = [e for e in events_by_day.get("unknown", []) if e.get("title") not in used_titles]

            # Choose candidates to assemble blocks
            # Prefer events closest to origin first if distances available
            def sort_by_distance(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
                return sorted(
                    items,
                    key=lambda x: (x.get("distance_miles") is None, x.get("distance_miles") or 0.0),
                )

            day_events_sorted = sort_by_distance(day_events)
            food_all = [c for c in candidates if c.get("category") == "food"]
            food_sorted = sort_by_distance(food_all)
            day_candidates = list(day_events_sorted) + list(food_sorted)
            activities = _pick_non_overlapping_blocks(
                day=day_dt,
                candidates=day_candidates,
                env_preference=request.preferences.environment,
                weather_day_info=day_weather,
            )

            # Track used event to diversify options
            for a in activities:
                if a.category != "food" and a.name:
                    used_titles.add(a.name)

            days.append(DayPlan(date=day_dt, activities=activities))

        # Skip empty plans (no activities at all)
        total_acts = sum(len(d.activities) for d in days)
        if total_acts == 0:
            continue

        options.append(
            ItineraryResponse(
                title=f"Plan {opt_idx + 1}: {request.city}",
                days=days,
                summary="Auto-generated from VisitPgh & Ticketmaster events, Yelp picks, weather, and distance preferences.",
                warnings=warnings.copy(),
                sources=used_sources.copy(),
            )
        )

    return ItineraryOptionsResponse(options=options, warnings=warnings, used_sources=used_sources)


def build_itinerary(request: ItineraryRequest) -> ItineraryResponse:
    """Backward-compatible single-plan builder.

    Uses the options builder and returns the first option if available,
    otherwise falls back to a very small placeholder for compatibility with
    existing tests.
    """
    options = build_itinerary_options(request)
    if options.options:
        return options.options[0]

    # Final fallback: minimal non-empty itinerary to avoid breaking existing smoke test
    days: List[DayPlan] = []
    for dt in _daterange(request.start_date, request.end_date):
        days.append(
            DayPlan(
                date=dt,
                activities=[
                    Activity(
                        name="Explore Downtown",
                        category="walk",
                        notes="Fallback due to unavailable data sources.",
                        source="fallback",
                    )
                ],
            )
        )
    return ItineraryResponse(
        title=f"Fallback Weekend in {request.city}",
        days=days,
        summary="Some data sources were unavailable; showing minimal plan.",
        warnings=options.warnings,
        sources=options.used_sources,
    )
