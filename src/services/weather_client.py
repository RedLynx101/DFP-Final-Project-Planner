"""
Title: Weather Client Service
Team: Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks
Date: 2025-09-11
Summary: Fetches weather forecast and provides an outdoor suitability score.
Disclaimer: This file includes AI-assisted content (GPT-5); reviewed and approved by the Purple Turtles team.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import httpx

from ..core.config import get_settings


OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/forecast"  # 3-hourly 5-day


def _geocode_city_to_coords(city: str) -> Optional[Dict[str, float]]:
    # Minimal mapping for Pittsburgh; could be expanded or use Maps API.
    lowered = city.lower()
    if "pittsburgh" in lowered:
        return {"lat": 40.4406, "lon": -79.9959}
    return None


def fetch_forecast(city: str, now: Optional[datetime] = None) -> Dict[str, Any]:
    settings = get_settings()
    coords = _geocode_city_to_coords(city)
    if not coords:
        raise ValueError("Unsupported city for forecast; only Pittsburgh supported in MVP")

    params = {
        "lat": coords["lat"],
        "lon": coords["lon"],
        "appid": settings.weather_api_key,
        "units": "imperial",
    }
    with httpx.Client(timeout=10) as client:
        resp = client.get(OPENWEATHER_URL, params=params)
        resp.raise_for_status()
        data = resp.json()

    return data


def outdoor_suitability(score_inputs: Dict[str, Any]) -> float:
    temp_f = score_inputs.get("temp_f")
    wind_mph = score_inputs.get("wind_mph", 0)
    precip_prob = score_inputs.get("precip_prob", 0)  # 0..1

    if temp_f is None:
        return 0.5

    score = 1.0
    # Temperature comfort window
    if temp_f < 40:
        score -= 0.4
    elif temp_f < 55:
        score -= 0.2
    elif temp_f > 90:
        score -= 0.5
    elif temp_f > 80:
        score -= 0.2

    # Wind penalty
    if wind_mph > 25:
        score -= 0.3
    elif wind_mph > 15:
        score -= 0.15

    # Precipitation probability penalty
    score -= min(precip_prob, 1.0) * 0.6

    return max(0.0, min(1.0, score))


def map_forecast_to_days(forecast: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """Aggregate 3-hourly forecast into per-day summary with outdoor suitability.

    Returns mapping date_str -> { temp_avg_f, wind_avg_mph, precip_prob_avg, suitability }
    """
    buckets: Dict[str, List[Dict[str, Any]]] = {}

    for item in forecast.get("list", []):
        ts = item.get("dt")
        if ts is None:
            continue
        dt = datetime.fromtimestamp(ts, tz=timezone.utc)
        ds = dt.date().isoformat()
        main = item.get("main", {})
        wind = item.get("wind", {})
        weather = item.get("weather", [{}])[0] or {}
        pop = item.get("pop", 0)
        buckets.setdefault(ds, []).append(
            {
                "temp_f": main.get("temp"),
                "wind_mph": wind.get("speed", 0),
                "precip_prob": pop,
                "weather": weather.get("main"),
            }
        )

    summary: Dict[str, Dict[str, Any]] = {}
    for ds, items in buckets.items():
        if not items:
            continue
        temp_vals = [i.get("temp_f") for i in items if i.get("temp_f") is not None]
        wind_vals = [i.get("wind_mph", 0) for i in items]
        pop_vals = [i.get("precip_prob", 0) for i in items]
        temp_avg = sum(temp_vals) / len(temp_vals) if temp_vals else None
        wind_avg = sum(wind_vals) / len(wind_vals) if wind_vals else 0
        pop_avg = sum(pop_vals) / len(pop_vals) if pop_vals else 0
        suitability = outdoor_suitability(
            {"temp_f": temp_avg, "wind_mph": wind_avg, "precip_prob": pop_avg}
        )
        summary[ds] = {
            "temp_avg_f": temp_avg,
            "wind_avg_mph": wind_avg,
            "precip_prob_avg": pop_avg,
            "suitability": suitability,
        }

    return summary

