"""
Title: Maps Client (Geocoding + Distance) — Flat Layout
Team: Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks
Date: 2025-09-15
Summary: Provides geocoding of addresses to lat/lon and distance estimation. Uses
        Google Maps if configured; otherwise falls back to simple haversine.
Disclaimer: This file includes AI-assisted content (GPT-5); reviewed and approved by the Purple Turtles team.
"""

from __future__ import annotations

from math import radians, cos, sin, asin, sqrt
from typing import Any, Dict, List, Optional

import httpx

from config import get_settings


GOOGLE_GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
GOOGLE_DISTANCE_MATRIX_URL = "https://maps.googleapis.com/maps/api/distancematrix/json"


def _haversine_miles(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius_miles = 3958.8
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return radius_miles * c


def geocode_address(address: str) -> Optional[Dict[str, float]]:
    # Known local addresses fallback (works without Google Maps)
    lowered = address.lower()
    if "hamburg hall" in lowered or "4800 forbes" in lowered or "carnegie mellon" in lowered or "cmu" in lowered:
        # Hamburg Hall / CMU vicinity
        return {"lat": 40.4439, "lon": -79.9430}

    settings = get_settings()
    if settings.maps_provider == "google" and settings.maps_api_key and not settings.maps_api_key.startswith("changeme"):
        params = {"address": address, "key": settings.maps_api_key}
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.get(GOOGLE_GEOCODE_URL, params=params)
                resp.raise_for_status()
                data = resp.json()
            if data.get("status") == "OK" and data.get("results"):
                loc = data["results"][0]["geometry"]["location"]
                return {"lat": float(loc["lat"]), "lon": float(loc["lng"])}
        except Exception:
            return None
    return None


def _format_coords(coords: Dict[str, float]) -> str:
    return f"{coords['lat']},{coords['lon']}"


def distance_matrix_miles(origins: List[Dict[str, float]], destinations: List[Dict[str, float]]) -> List[List[Dict[str, Any]]]:
    """Return matrix of {distance_miles, duration_minutes} for each origin->destination.

    Falls back to haversine with naive 25 mph estimate if Google is not configured.
    """
    settings = get_settings()

    if (
        settings.maps_provider == "google"
        and settings.maps_api_key
        and not settings.maps_api_key.startswith("changeme")
    ):
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.get(
                    GOOGLE_DISTANCE_MATRIX_URL,
                    params={
                        "origins": "|".join(_format_coords(o) for o in origins),
                        "destinations": "|".join(_format_coords(d) for d in destinations),
                        "key": settings.maps_api_key,
                        "units": "imperial",
                        "mode": "driving",
                    },
                )
                resp.raise_for_status()
                data = resp.json()
            rows = data.get("rows", [])
            result: List[List[Dict[str, Any]]] = []
            for row in rows:
                row_vals: List[Dict[str, Any]] = []
                for element in row.get("elements", []):
                    if element.get("status") == "OK":
                        dist_miles = element["distance"]["value"] / 1609.344
                        dur_min = int(round(element["duration"]["value"] / 60))
                        row_vals.append({"distance_miles": dist_miles, "duration_minutes": dur_min})
                    else:
                        row_vals.append({"distance_miles": None, "duration_minutes": None})
                result.append(row_vals)
            return result
        except Exception:
            pass

    # Haversine fallback with naive speed assumption
    result: List[List[Dict[str, Any]]] = []
    for o in origins:
        row: List[Dict[str, Any]] = []
        for d in destinations:
            dist = _haversine_miles(o["lat"], o["lon"], d["lat"], d["lon"])
            duration_minutes = int(round((dist / 25.0) * 60))  # assume 25 mph mixed travel
            row.append({"distance_miles": dist, "duration_minutes": duration_minutes})
        result.append(row)
    return result


