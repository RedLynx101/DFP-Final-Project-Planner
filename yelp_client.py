"""
Title: Yelp Client Service (Flat Layout)
Team: Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks
Date: 2025-09-15
Summary: Lightweight Yelp Fusion API client for food business search.
Disclaimer: This file includes AI-assisted content (GPT-5); reviewed and approved by the Purple Turtles team.
"""

from typing import Any, Dict, List, Optional
import httpx
from config import get_settings


YELP_BASE_URL = "https://api.yelp.com/v3"


def _auth_headers() -> Dict[str, str]:
    settings = get_settings()
    return {"Authorization": f"Bearer {settings.yelp_api_key}"}


def search_food(
    query: str,
    location: str = "Pittsburgh, PA",
    limit: int = 5,
    price: Optional[str] = None,
) -> Dict[str, Any]:
    """Search Yelp businesses for food-related queries.

    Returns a simplified payload with selected fields for each business.
    """
    params: Dict[str, Any] = {
        "term": query,
        "location": location,
        "limit": max(1, min(limit, 50)),
        "categories": "food,restaurants",
    }
    if price:
        params["price"] = price  # e.g., "1,2" (Yelp's $..$$$ mapping)

    with httpx.Client(timeout=10) as client:
        resp = client.get(f"{YELP_BASE_URL}/businesses/search", params=params, headers=_auth_headers())
        resp.raise_for_status()
        data = resp.json()

    simplified: List[Dict[str, Any]] = []
    for b in data.get("businesses", []):
        simplified.append(
            {
                "name": b.get("name"),
                "rating": b.get("rating"),
                "price": b.get("price"),
                "phone": b.get("display_phone"),
                "url": b.get("url"),
                "categories": [c.get("title") for c in b.get("categories", [])],
                "location": ", ".join(filter(None, b.get("location", {}).get("display_address", []))),
                "coordinates": b.get("coordinates"),
                "review_count": b.get("review_count"),
                "photo": b.get("image_url"),
            }
        )

    return {"query": query, "location": location, "results": simplified}


