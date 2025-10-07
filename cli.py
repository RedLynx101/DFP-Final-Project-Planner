"""
Title: Console CLI for Weekender
Team: Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks
CMU IDs: nhicks, aadyaaga, yepeng, wendyl2
Date: 2025-09-15
Summary: Command-line interface to build itineraries without a web server.
Disclaimer: This file includes AI-assisted content (GPT-5); reviewed and approved by the Purple Turtles team.
"""

from __future__ import annotations

import argparse
import json
from typing import Any

from config import get_settings
from logging_config import configure_logging
from itinerary import ItineraryRequest
from planner import build_itinerary, build_itinerary_options


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a Pittsburgh weekend itinerary from the console"
    )
    parser.add_argument("--city", default="Pittsburgh, PA", help="City name")
    parser.add_argument("--user-address", default="Hamburg Hall, 4800 Forbes Ave, Pittsburgh, PA 15213", help="Origin address")
    parser.add_argument("--max-distance-miles", type=float, default=5.0, help="Max distance in miles from origin")
    parser.add_argument("--environment", default="either", choices=["indoor", "outdoor", "either"], help="Environment preference")
    parser.add_argument("--options", type=int, default=1, help="Number of diversified options to produce (1 for single)")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of pretty text")
    return parser.parse_args()


def itinerary_request_from_args(args: argparse.Namespace) -> ItineraryRequest:
    return ItineraryRequest(
        city=args.city,
        preferences={
            "environment": args.environment,
        },
        user_address=args.user_address,
        max_distance_miles=args.max_distance_miles,
    )


def print_pretty(data: Any) -> None:
    # Simple pretty-printer for the core itinerary
    title = data.get("title") if isinstance(data, dict) else getattr(data, "title", None)
    if title:
        print(f"\n=== {title} ===\n")
    days = data.get("days") if isinstance(data, dict) else getattr(data, "days", [])
    for day in days or []:
        date = day.get("date") if isinstance(day, dict) else getattr(day, "date", None)
        print(f"# {date}")
        activities = day.get("activities") if isinstance(day, dict) else getattr(day, "activities", [])
        for act in activities or []:
            name = act.get("name") if isinstance(act, dict) else getattr(act, "name", None)
            cat = act.get("category") if isinstance(act, dict) else getattr(act, "category", None)
            env = act.get("environment") if isinstance(act, dict) else getattr(act, "environment", None)
            dist = act.get("distance_miles") if isinstance(act, dict) else getattr(act, "distance_miles", None)
            print(f"- {name} [{cat}] env={env} dist={dist}")
        print()
    warnings = data.get("warnings") if isinstance(data, dict) else getattr(data, "warnings", [])
    if warnings:
        print("Warnings:")
        for w in warnings:
            print(f"  - {w}")


def main() -> None:
    configure_logging()
    _ = get_settings()  # ensure .env loaded consistently
    args = parse_args()
    req = itinerary_request_from_args(args)

    if args.options and args.options > 1:
        resp = build_itinerary_options(req)
        if args.json:
            print(json.dumps(resp.model_dump(), indent=2, default=str))
        else:
            for i, opt in enumerate(resp.options, start=1):
                print(f"\n===== Option {i} =====")
                print_pretty(opt.model_dump())
    else:
        resp = build_itinerary(req)
        if args.json:
            print(json.dumps(resp.model_dump(), indent=2, default=str))
        else:
            print_pretty(resp.model_dump())


if __name__ == "__main__":
    main()


