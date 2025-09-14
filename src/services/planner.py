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
from .classifier import classify_environment, classify_environments_batch_sync
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


def _estimate_activity_cost(item: Dict[str, Any], budget_level: str = "medium") -> Optional[float]:
    """Estimate cost for an activity based on type, source, and budget preferences."""
    category = item.get("category", "").lower()
    source = item.get("source", "")
    
    # Yelp food price mapping - based on Yelp's price levels
    if source == "yelp" and item.get("price"):
        price_level = item.get("price", "")
        price_map = {
            "$": (8, 15),      # Casual/fast food
            "$$": (15, 30),    # Mid-range
            "$$$": (30, 60),   # Upscale
            "$$$$": (60, 120), # High-end
        }
        if price_level in price_map:
            low, high = price_map[price_level]
            # Adjust based on budget preference
            if budget_level == "low":
                return low
            elif budget_level == "high":
                return high
            else:  # medium
                return (low + high) / 2
    
    # Default estimates by category and budget level
    estimates = {
        "food": {"low": 12, "medium": 25, "high": 45},
        "event": {"low": 0, "medium": 15, "high": 35},
        "museum": {"low": 10, "medium": 18, "high": 25},
        "activity": {"low": 5, "medium": 20, "high": 40},
        "entertainment": {"low": 8, "medium": 25, "high": 50},
        "shopping": {"low": 15, "medium": 50, "high": 100},
        "outdoor": {"low": 0, "medium": 10, "high": 25},
        "park": {"low": 0, "medium": 5, "high": 15},
    }
    
    # Look for category match
    for key in estimates:
        if key in category:
            return estimates[key].get(budget_level, estimates[key]["medium"])
    
    # Default fallback
    return estimates["activity"].get(budget_level, estimates["activity"]["medium"])


def _get_weather_icon(weather_info: Optional[Dict[str, Any]]) -> str:
    """Convert weather information to appropriate emoji icon."""
    if not weather_info:
        return "🌤️"  # Default partly cloudy
    
    temp_f = weather_info.get("temp_avg_f", 70)
    precip_prob = weather_info.get("precip_prob_avg", 0)
    suitability = weather_info.get("suitability", 0.5)
    
    # High precipitation probability
    if precip_prob > 0.6:
        return "🌧️"  # Rain
    elif precip_prob > 0.3:
        return "⛅"   # Partly cloudy with chance of rain
    
    # Temperature-based icons
    if temp_f < 40:
        return "🥶"   # Very cold
    elif temp_f < 60:
        return "🌤️"  # Cool but pleasant
    elif temp_f > 85:
        return "🔥"   # Hot
    elif temp_f > 75:
        return "☀️"   # Warm and sunny
    else:
        return "😊"   # Perfect weather
    
    # Suitability-based fallback
    if suitability > 0.7:
        return "☀️"   # Great weather
    elif suitability > 0.4:
        return "🌤️"  # Decent weather
    else:
        return "⛅"   # Poor weather


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
    budget_level: str = "medium",
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

    def to_activity(item: Dict[str, Any], start_h: int, end_h: int, budget_level: str = "medium") -> Activity:
        # Calculate cost estimate
        cost_estimate = _estimate_activity_cost(item, budget_level)
        
        # Get weather icon if weather info is available
        weather_icon = _get_weather_icon(weather_day_info)
        
        return Activity(
            name=item.get("name") or item.get("title") or "Activity",
            category=item.get("category") or item.get("type") or "activity",
            address=item.get("address"),
            start_time=datetime(day.year, day.month, day.day, start_h, 0).time(),
            end_time=datetime(day.year, day.month, day.day, end_h, 0).time(),
            cost_estimate=cost_estimate,
            notes=item.get("notes"),
            external_url=item.get("url"),
            source=item.get("source"),
            environment=item.get("environment"),
            coordinates=item.get("coordinates"),
            distance_miles=item.get("distance_miles"),
            travel_time_minutes=item.get("duration_minutes"),
            weather_info=weather_day_info,
            weather_icon=weather_icon,
        )

    # Morning: breakfast
    if food:
        chosen.append(to_activity(food[0], *blocks[0][1], budget_level))
    # Afternoon: event
    if events:
        chosen.append(to_activity(events[0], *blocks[1][1], budget_level))
    # Evening: dinner
    if len(food) > 1:
        chosen.append(to_activity(food[1], *blocks[2][1], budget_level))
    elif food:
        # reuse breakfast place for dinner only if no alternative
        chosen.append(to_activity(food[0], *blocks[2][1], budget_level))

    return chosen


def _collect_candidates(
    city: str,
    interests: List[str],
    env_pref: str,
    start: datetime,
    end: datetime,
    origin_coords: Optional[Dict[str, float]] = None,
    max_distance_miles: Optional[float] = None,
) -> Tuple[List[Dict[str, Any]], List[str], Dict[str, int]]:
    warnings: List[str] = []
    sources: Dict[str, int] = {}
    candidates: List[Dict[str, Any]] = []

    # Collect all events first, then classify them concurrently for speed
    event_candidates = []
    classification_texts = []
    
    # VisitPgh events (web-scraped)
    try:
        events_payload = fetch_this_week_events()
        for e in events_payload.get("events", []):
            title = e.get("title") or ""
            details = e.get("details") or ""
            url = e.get("url")
            day_name = _parse_day_from_text(f"{title} {details}")
            event_candidate = {
                "title": title,
                "category": "event",
                "type": "event",
                "notes": details,
                "url": url,
                "source": "visitpgh",
                "day_name": day_name,
            }
            event_candidates.append(event_candidate)
            classification_texts.append(f"{title} {details}")
        sources["visitpgh"] = len(events_payload.get("events", []))
    except Exception as exc:
        warnings.append(f"visitpgh_unavailable: {exc}")

    # Ticketmaster events (API) — restricted to requested window and proximity if available
    try:
        if origin_coords is not None:
            tm_payload = fetch_events_ticketmaster(
                city=None,
                lat=origin_coords.get("lat"),
                lon=origin_coords.get("lon"),
                radius_miles=int(max_distance_miles or 10),
                start=start,
                end=end,
            )
        else:
            tm_payload = fetch_events_ticketmaster(city=city.split(",")[0], start=start, end=end)
        for e in tm_payload.get("events", []):
            title = e.get("title") or ""
            details = e.get("details") or ""
            url = e.get("url")
            day_name = _weekday_from_iso_datetime(e.get("start_datetime"))
            event_candidate = {
                "title": title,
                "category": "event",
                "type": "event",
                "notes": details,
                "url": url,
                "source": "ticketmaster",
                "day_name": day_name,
                "coordinates": e.get("coordinates"),
            }
            event_candidates.append(event_candidate)
            classification_texts.append(f"{title} {details}")
        sources["ticketmaster"] = len(tm_payload.get("events", []))
    except Exception as exc:
        warnings.append(f"ticketmaster_unavailable: {exc}")

    # Classify all events concurrently (much faster!)
    if classification_texts:
        try:
            environments = classify_environments_batch_sync(classification_texts)
            for i, env in enumerate(environments):
                event_candidates[i]["environment"] = env
        except Exception as exc:
            warnings.append(f"classification_batch_failed: {exc}")
            # Fallback to sequential classification
            for candidate in event_candidates:
                title = candidate.get("title") or ""
                notes = candidate.get("notes") or ""
                candidate["environment"] = classify_environment(f"{title} {notes}")

    # Add classified events to candidates
    candidates.extend(event_candidates)

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
                # retain a fraction of non-matching events to preserve variety
                # simple heuristic: keep every 3rd non-matching event
                if (len(keep) % 3) == 0:
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

    # Determine origin early to pass into candidate collection for better filtering
    origin_coords: Optional[Dict[str, float]] = None
    if request.user_address:
        origin_coords = geocode_address(request.user_address)
        if origin_coords is None:
            origin_coords = _pittsburgh_coords()

    candidates, w2, s2 = _collect_candidates(
        city=request.city,
        interests=request.preferences.interests,
        env_pref=request.preferences.environment,
        start=request.start_date,
        end=request.end_date,
        origin_coords=origin_coords,
        max_distance_miles=request.max_distance_miles,
    )
    warnings.extend(w2)
    for k, v in s2.items():
        used_sources[k] = used_sources.get(k, 0) + v

    # origin_coords already computed above

    # Attach distances from origin when possible and filter by max distance if requested
    if origin_coords is not None:
        # For items without coords, attempt naive geocode by address once
        for c in candidates:
            if not c.get("coordinates") and c.get("address"):
                gc = geocode_address(c["address"])  # may be None
                if gc:
                    c["coordinates"] = gc

        # Build destinations while tracking which items truly had coordinates
        had_coords: list[bool] = []
        destinations = []
        for c in candidates:
            coords = c.get("coordinates")
            if coords:
                had_coords.append(True)
                destinations.append(coords)
            else:
                had_coords.append(False)
                destinations.append(origin_coords)  # placeholder to keep matrix shape

        matrix = distance_matrix_miles([origin_coords], destinations)
        if matrix:
            row0 = matrix[0]
            for idx, c in enumerate(candidates):
                dm = row0[idx]
                # Only assign distances if we had true destination coordinates
                if had_coords[idx]:
                    c["distance_miles"] = dm.get("distance_miles")
                    c["duration_minutes"] = dm.get("duration_minutes")
                else:
                    c["distance_miles"] = None
                    c["duration_minutes"] = None

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
            if "unknown" not in events_by_day:
                events_by_day["unknown"] = []
            events_by_day["unknown"].append(c)

    # For each option, pick a different featured event when possible
    global_used_event_titles: set[str] = set()
    global_used_food_names: set[str] = set()
    for opt_idx in range(3):
        days: List[DayPlan] = []
        used_titles: set[str] = set()  # per-option events used across days
        used_foods: set[str] = set()  # per-option foods used across days
        for day_dt in day_dates:
            dn = WEEKDAY_NAMES[day_dt.weekday()]
            day_weather = daily_weather.get(day_dt.date().isoformat())
            # Fallback: if exact date not available, use the closest available weather data
            if not day_weather and daily_weather:
                available_dates = list(daily_weather.keys())
                if available_dates:
                    # Use the last available date as a fallback (most relevant for future dates)
                    day_weather = daily_weather[available_dates[-1]]

            # Candidate pool for this day
            day_events = [
                e
                for e in events_by_day.get(dn, [])
                if e.get("title") not in used_titles and e.get("title") not in global_used_event_titles
            ]
            if not day_events:
                day_events = [
                    e
                    for e in events_by_day.get("unknown", [])
                    if e.get("title") not in used_titles and e.get("title") not in global_used_event_titles
                ]

            # Choose candidates to assemble blocks
            # Prefer events closest to origin first if distances available
            def sort_by_distance(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
                return sorted(
                    items,
                    key=lambda x: (x.get("distance_miles") is None, x.get("distance_miles") or 0.0),
                )

            day_events_sorted = sort_by_distance(day_events)
            food_all = [
                c
                for c in candidates
                if c.get("category") == "food"
                and c.get("name") not in used_foods
                and c.get("name") not in global_used_food_names
            ]
            food_sorted = sort_by_distance(food_all)

            # Diversify options by rotating the sorted lists per option index
            if day_events_sorted:
                ev_off = opt_idx % len(day_events_sorted)
                rotated_events = day_events_sorted[ev_off:] + day_events_sorted[:ev_off]
            else:
                rotated_events = []

            if food_sorted:
                food_off = opt_idx % len(food_sorted)
                rotated_food = food_sorted[food_off:] + food_sorted[:food_off]
            else:
                rotated_food = []

            day_candidates = list(rotated_events) + list(rotated_food)
            activities = _pick_non_overlapping_blocks(
                day=day_dt,
                candidates=day_candidates,
                env_preference=request.preferences.environment,
                weather_day_info=day_weather,
                budget_level=request.preferences.budget_level,
            )

            # Track used items to diversify options
            for a in activities:
                if a.category != "food" and a.name:
                    used_titles.add(a.name)
                if a.category == "food" and a.name:
                    used_foods.add(a.name)

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

        # Update global usage to steer subsequent options away from previously used items
        for d in days:
            for a in d.activities:
                if a.category != "food" and a.name:
                    global_used_event_titles.add(a.name)
                if a.category == "food" and a.name:
                    global_used_food_names.add(a.name)

    # Deduplicate identical options (can occur when data is sparse)
    unique: List[ItineraryResponse] = []
    seen_signatures: set[Tuple[Tuple[str, str], ...]] = set()
    for opt in options:
        signature: Tuple[Tuple[str, str], ...] = tuple(
            (a.name or "", a.category or "") for d in opt.days for a in d.activities
        )
        if signature not in seen_signatures:
            seen_signatures.add(signature)
            unique.append(opt)

    return ItineraryOptionsResponse(options=unique, warnings=warnings, used_sources=used_sources)


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
                        environment="outdoor",
                        coordinates=None,
                        distance_miles=None,
                        travel_time_minutes=None,
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
