"""
Title: Ticketmaster Discovery API Client
Team: Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks
Date: 2025-09-12
Summary: Lightweight client for Ticketmaster Discovery API to fetch events by city
         and date range for Pittsburgh planning.
Disclaimer: This file includes AI-assisted content (GPT-5); reviewed and approved by the Purple Turtles team.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

import httpx

from ..core.config import get_settings


TM_BASE_URL = "https://app.ticketmaster.com/discovery/v2/events.json"


def _format_iso_z(dt: datetime) -> str:
    # Ensure UTC Z format
    if dt.tzinfo is None:
        return dt.isoformat(timespec="seconds") + "Z"
    return dt.astimezone().isoformat(timespec="seconds").replace("+00:00", "Z")


def fetch_events_ticketmaster(
    city: Optional[str] = "Pittsburgh",
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    radius_miles: Optional[int] = 25,
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
    size: int = 50,
) -> Dict[str, Any]:
    """Fetch events via Ticketmaster Discovery API.

    Returns simplified list: [{title, details, url, start_datetime, venue, coordinates}]
    """
    settings = get_settings()
    if not settings.ticketmaster_api_key or settings.ticketmaster_api_key.startswith("changeme"):
        return {"source": TM_BASE_URL, "events": []}

    params: Dict[str, Any] = {
        "apikey": settings.ticketmaster_api_key,
        "size": min(max(size, 1), 200),
        "sort": "date,asc",
    }

    if start:
        params["startDateTime"] = _format_iso_z(start)
    if end:
        params["endDateTime"] = _format_iso_z(end)

    if lat is not None and lon is not None:
        params["latlong"] = f"{lat},{lon}"
        if radius_miles is not None:
            params["radius"] = radius_miles
            params["unit"] = "miles"
    elif city:
        params["city"] = city

    with httpx.Client(timeout=10) as client:
        resp = client.get(TM_BASE_URL, params=params)
        resp.raise_for_status()
        data = resp.json()

    events: List[Dict[str, Any]] = []
    embedded = data.get("_embedded", {})
    for e in embedded.get("events", []):
        title = e.get("name")
        url = e.get("url")
        dates = e.get("dates", {})
        start_dt = dates.get("start", {}).get("dateTime")
        venues = (e.get("_embedded", {}) or {}).get("venues", [])
        venue_name = venues[0].get("name") if venues else None
        coords = None
        if venues and venues[0].get("location"):
            try:
                lat_val = float(venues[0]["location"]["latitude"])  # type: ignore[index]
                lon_val = float(venues[0]["location"]["longitude"])  # type: ignore[index]
                coords = {"lat": lat_val, "lon": lon_val}
            except Exception:
                coords = None
        # Prefer human-readable fields; avoid falling back to opaque event IDs
        info = e.get("info") or e.get("pleaseNote") or None
        events.append(
            {
                "title": title,
                "details": info,
                "url": url,
                "start_datetime": start_dt,
                "venue": venue_name,
                "coordinates": coords,
                "source": "ticketmaster",
            }
        )

    return {"source": TM_BASE_URL, "events": events}


