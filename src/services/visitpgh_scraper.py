"""
Title: VisitPittsburgh Scraper
Team: Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks
Date: 2025-09-11
Summary: Scrapes 'This Week in Pittsburgh' events from VisitPittsburgh.
Disclaimer: This file includes AI-assisted content (GPT-5); reviewed and approved by the Purple Turtles team.
"""

from typing import Any, Dict, List
import httpx
from bs4 import BeautifulSoup


VISIT_PGH_URL = "https://www.visitpittsburgh.com/events-festivals/this-week-in-pittsburgh/"


def fetch_this_week_events() -> Dict[str, Any]:
    """Scrape VisitPittsburgh's 'This Week' page and return a list of event dicts.

    This is best-effort scraping and may need adjustments if the page structure changes.
    """
    with httpx.Client(timeout=15) as client:
        resp = client.get(VISIT_PGH_URL, headers={"User-Agent": "weekender/1.0"})
        resp.raise_for_status()
        html = resp.text

    soup = BeautifulSoup(html, "lxml")

    events: List[Dict[str, Any]] = []

    # Heuristic extraction: find prominent headings under the main content and capture sibling text.
    # Fallback parses links within sections that look like event items.
    main = soup.find("main") or soup

    # Collect h2/h3 headings that look like event titles
    for heading in main.select("h2, h3"):
        title = heading.get_text(strip=True)
        if not title:
            continue
        # Skip obvious non-event headings
        lowered = title.lower()
        if any(k in lowered for k in ["navigation", "happening this week", "ongoing", "get the details", "contact", "privacy", "start planning"]):
            continue

        # Try to locate a nearby date/venue text in the next sibling(s)
        info_text = None
        for sib in heading.find_all_next(["p", "strong", "span"], limit=5):
            txt = sib.get_text(" ", strip=True)
            if txt and len(txt) > 6:
                info_text = txt
                break

        link = None
        a = heading.find("a") or heading.find_next("a")
        if a and a.get("href"):
            link = a["href"]

        events.append({"title": title, "details": info_text, "url": link})

    # De-dup on title
    seen = set()
    unique: List[Dict[str, Any]] = []
    for e in events:
        t = e.get("title")
        if t and t not in seen:
            unique.append(e)
            seen.add(t)

    return {"source": VISIT_PGH_URL, "events": unique[:25]}


