"""
Title: VisitPittsburgh Scraper Test
Team: Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks
Date: 2025-09-12
Summary: Integration test that exercises the VisitPittsburgh scraper and prints a short summary.
Disclaimer: This file includes AI-assisted content (GPT-5); reviewed and approved by the Purple Turtles team.

Test Script: python -c "from src.services.visitpgh_scraper import fetch_this_week_events; import json; d=fetch_this_week_events(); print('events:', len(d.get('events', []))); print(json.dumps(d.get('events', [])[:5], indent=2))"
"""

from src.services.visitpgh_scraper import fetch_this_week_events


def test_visitpgh_scraper_print_results():
    """
    Integration test for the VisitPittsburgh scraper with explicit error handling.
    """
    try:
        data = fetch_this_week_events()
    except Exception as e:
        print(f"Error fetching events: {e}")
        assert False, f"fetch_this_week_events() raised an exception: {e}"

    if not isinstance(data, dict):
        print("Returned data is not a dictionary.")
        assert False, "Returned data is not a dictionary."

    if "events" not in data:
        print("Key 'events' not found in data.")
        assert False, "Key 'events' not found in data."

    if not isinstance(data["events"], list):
        print("'events' is not a list.")
        assert False, "'events' is not a list."

    events = data["events"]
    print(f"Total events scraped: {len(events)}")

    if len(events) == 0:
        print("No events found.")
        assert False, "No events found."
        
    for i, e in enumerate(events[:5]):
        if not isinstance(e, dict):
            print(f"Event {i} is not a dictionary: {e}")
            continue
        title = e.get("title", "<No Title>")
        url = e.get("url", "<No URL>")
        details = e.get("details") or ""
        snippet = details[:100].replace("\n", " ")
        print(f"- {title} | {url} | {snippet}")
