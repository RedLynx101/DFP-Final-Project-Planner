"""
Title: Console CLI for Weekender (Interactive Menu Version)
Team: Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks
CMU IDs: nhicks, aadyaaga, yepeng, wendyl2
Date: 2025-09-15
Summary: Interactive command-line interface to build itineraries without a web server.
Disclaimer: This file includes AI-assisted content (GPT-5); reviewed and approved by the Purple Turtles team.
"""

from __future__ import annotations

import json
import sys
import time
from typing import Any, Optional

from config import get_settings
from logging_config import configure_logging
from itinerary import ItineraryRequest, Preference
from planner import build_itinerary, build_itinerary_options
from yelp_client import search_food
from visitpgh_scraper import fetch_this_week_events


# ============================================================================
# ASCII ART & ANIMATIONS
# ============================================================================

TITLE_ART = r"""
╔═════════════════════════════════════════════════════════════════════════════════╗
║                                                                                 ║
║   ██╗    ██╗███████╗███████╗██╗  ██╗███████╗███╗   ██╗██████╗ ███████╗██████╗   ║
║   ██║    ██║██╔════╝██╔════╝██║ ██╔╝██╔════╝████╗  ██║██╔══██╗██╔════╝██╔══██╗  ║
║   ██║ █╗ ██║█████╗  █████╗  █████╔╝ █████╗  ██╔██╗ ██║██║  ██║█████╗  ██████╔╝  ║
║   ██║███╗██║██╔══╝  ██╔══╝  ██╔═██╗ ██╔══╝  ██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗  ║
║   ╚███╔███╔╝███████╗███████╗██║  ██╗███████╗██║ ╚████║██████╔╝███████╗██║  ██║  ║
║    ╚══╝╚══╝ ╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝  ║
║                                                                                 ║
║              Pittsburgh Plan-o-matic ~ Weekend Itinerary Builder                ║
║                                                                                 ║
╚═════════════════════════════════════════════════════════════════════════════════╝
"""

TURTLE_ART = r"""
..................................................
......................:^^^~^^:....................
.....................:!!7777!7^...................
.....................!7J0---0!7:..................
.............:^~!^..:777!~~~777!..................
.............~777!:.:~!!!---!!~^..................
.............:~777~:.:~?JJ?J?7^...................
...............:~!77777!!77!!7J?^.................
..................:!J?!~~~~~~~7??:................
...................J?~~~~~~~~~~!7!^...............
..................:J!~~~~~~~~~~~!77!^.............
..................:J!~~~~~~~~~~~??!!^.............
...................!J!~~~~~~~~~7J^................
....................~77!!777!777^.................
.....................~77?!^7777:..................
.....................!777~:7777^..................
.....................!777!^7777~..................
.....................^~~~~^~~~~^..................
..................................................
              Purple Turtles Team 🐢
"""

CREDITS = """
╔══════════════════════════════════════════════════════════════════════════╗
║                         DEVELOPMENT TEAM                                 ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║   👤  Gwen Li          (wendyl2)   - Team Purple Turtles                ║
║   👤  Aadya Agarwal    (aadyaaga)  - Team Purple Turtles                ║
║   👤  Emma Peng        (yepeng)    - Team Purple Turtles                ║
║   👤  Noah Hicks       (nhicks)    - Team Purple Turtles                ║
║                                                                          ║
║   🎓  Carnegie Mellon University - Python Programming Class             ║
║   📅  Date: October 7, 2025                                             ║
║   🤖  AI-Assisted Development (GPT-5) - Human Reviewed & Approved       ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
"""

LOADING_FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]


def animate_loading(message: str, duration: float = 2.0) -> None:
    """Show a spinning loader animation."""
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        frame = LOADING_FRAMES[i % len(LOADING_FRAMES)]
        sys.stdout.write(f"\r{frame} {message}...")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write("\r" + " " * (len(message) + 10) + "\r")
    sys.stdout.flush()


def typewriter(text: str, delay: float = 0.02) -> None:
    """Print text with typewriter effect."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def clear_screen() -> None:
    """Clear console screen (cross-platform)."""
    import os
    os.system("cls" if os.name == "nt" else "clear")


def show_intro() -> None:
    """Display animated intro sequence."""
    clear_screen()
    print(TITLE_ART)
    time.sleep(0.5)
    print(TURTLE_ART)
    time.sleep(0.5)
    animate_loading("Initializing Weekender Console", duration=1.5)
    print(CREDITS)
    input("\n\n   Press ENTER to continue to main menu...")


# ============================================================================
# INPUT HELPERS
# ============================================================================

def get_input(prompt: str, default: Optional[str] = None) -> str:
    """Get user input with optional default."""
    if default:
        full_prompt = f"{prompt} [{default}]: "
    else:
        full_prompt = f"{prompt}: "
    value = input(full_prompt).strip()
    return value if value else (default or "")


def get_float_input(prompt: str, default: float) -> float:
    """Get float input with validation."""
    while True:
        val = get_input(prompt, str(default))
        try:
            return float(val)
        except ValueError:
            print(f"   ❌ Invalid number. Please try again.")


def get_int_input(prompt: str, default: int) -> int:
    """Get integer input with validation."""
    while True:
        val = get_input(prompt, str(default))
        try:
            return int(val)
        except ValueError:
            print(f"   ❌ Invalid integer. Please try again.")


def get_choice(prompt: str, choices: list[str], default: str) -> str:
    """Get choice from a list."""
    while True:
        val = get_input(f"{prompt} ({'/'.join(choices)})", default).lower()
        if val in choices:
            return val
        print(f"   ❌ Invalid choice. Choose from: {', '.join(choices)}")


# ============================================================================
# PRETTY OUTPUT
# ============================================================================

def print_separator(char: str = "═", length: int = 78) -> None:
    """Print a separator line."""
    print(char * length)


def print_header(text: str) -> None:
    """Print a fancy header."""
    print_separator()
    print(f"║ {text.center(74)} ║")
    print_separator()


def print_activity(act: Any, index: int) -> None:
    """Print a single activity in a pretty format."""
    name = act.get("name") if isinstance(act, dict) else getattr(act, "name", "Unknown")
    category = act.get("category") if isinstance(act, dict) else getattr(act, "category", "N/A")
    env = act.get("environment") if isinstance(act, dict) else getattr(act, "environment", "unknown")
    dist = act.get("distance_miles") if isinstance(act, dict) else getattr(act, "distance_miles", None)
    address = act.get("address") if isinstance(act, dict) else getattr(act, "address", None)
    url = act.get("external_url") if isinstance(act, dict) else getattr(act, "external_url", None)
    
    print(f"\n   🎯 Activity {index + 1}: {name}")
    print(f"      📁 Category: {category}")
    print(f"      🏠 Environment: {env}")
    if dist is not None:
        print(f"      📍 Distance: {dist:.2f} miles")
    if address:
        print(f"      🗺️  Address: {address}")
    if url:
        print(f"      🔗 URL: {url}")


def print_itinerary(data: Any) -> None:
    """Print itinerary in a pretty format."""
    title = data.get("title") if isinstance(data, dict) else getattr(data, "title", "Itinerary")
    days = data.get("days") if isinstance(data, dict) else getattr(data, "days", [])
    warnings = data.get("warnings") if isinstance(data, dict) else getattr(data, "warnings", [])
    
    print_header(title)
    
    for day_idx, day in enumerate(days or [], start=1):
        date = day.get("date") if isinstance(day, dict) else getattr(day, "date", "Unknown Date")
        activities = day.get("activities") if isinstance(day, dict) else getattr(day, "activities", [])
        
        print(f"\n📅 Day {day_idx}: {date}")
        print("─" * 78)
        
        if not activities:
            print("   ⚠️  No activities scheduled for this day.")
        else:
            for act_idx, act in enumerate(activities):
                print_activity(act, act_idx)
    
    if warnings:
        print("\n")
        print_header("⚠️  WARNINGS")
        for w in warnings:
            print(f"   • {w}")
    
    print_separator()


def print_events(events_data: dict[str, Any]) -> None:
    """Print events from VisitPittsburgh scraper."""
    source = events_data.get("source", "Unknown")
    events = events_data.get("events", [])
    
    print_header(f"This Week's Events (Source: {source})")
    
    if not events:
        print("   ⚠️  No events found.")
    else:
        for idx, event in enumerate(events, start=1):
            title = event.get("title", "Untitled")
            details = event.get("details")
            url = event.get("url")
            
            print(f"\n   🎉 Event {idx}: {title}")
            if details:
                print(f"      ℹ️  {details}")
            if url:
                print(f"      🔗 {url}")
    
    print_separator()


def print_food_results(food_data: dict[str, Any]) -> None:
    """Print Yelp food search results."""
    query = food_data.get("query", "")
    location = food_data.get("location", "")
    results = food_data.get("results", [])
    
    print_header(f"Food Search: '{query}' in {location}")
    
    if not results:
        print("   ⚠️  No results found.")
    else:
        for idx, biz in enumerate(results, start=1):
            name = biz.get("name", "Unknown")
            rating = biz.get("rating", "N/A")
            price = biz.get("price", "N/A")
            address = biz.get("location", "N/A")
            phone = biz.get("phone", "N/A")
            url = biz.get("url")
            
            print(f"\n   🍽️  Restaurant {idx}: {name}")
            print(f"      ⭐ Rating: {rating}")
            print(f"      💰 Price: {price}")
            print(f"      📍 Location: {address}")
            print(f"      ☎️  Phone: {phone}")
            if url:
                print(f"      🔗 {url}")
    
    print_separator()


# ============================================================================
# MENU OPTIONS
# ============================================================================

def option_build_itinerary() -> None:
    """Menu option: Build a single itinerary."""
    clear_screen()
    print_header("🗓️  BUILD WEEKEND ITINERARY")
    
    print("\n   Let's plan your perfect Pittsburgh weekend!\n")
    
    city = get_input("   🏙️  City", "Pittsburgh, PA")
    user_address = get_input("   🏠 Your starting address", "Hamburg Hall, 4800 Forbes Ave, Pittsburgh, PA 15213")
    max_distance = get_float_input("   📏 Max distance (miles)", 5.0)
    environment = get_choice("   🌤️  Environment preference", ["indoor", "outdoor", "either"], "either")
    budget = get_choice("   💵 Budget level", ["low", "medium", "high"], "medium")
    mobility = get_choice("   🚶 Mobility preference", ["walk", "transit", "drive"], "walk")
    
    print("\n")
    animate_loading("Building your perfect itinerary", duration=2.0)
    
    try:
        req = ItineraryRequest(
            city=city,
            user_address=user_address,
            max_distance_miles=max_distance,
            preferences=Preference(
                environment=environment,
                budget_level=budget,
                mobility=mobility,
            ),
        )
        resp = build_itinerary(req)
        print("\n✅ Itinerary generated successfully!\n")
        print_itinerary(resp.model_dump())
    except Exception as e:
        print(f"\n❌ Error building itinerary: {e}")
    
    input("\n\n   Press ENTER to return to main menu...")


def option_build_options() -> None:
    """Menu option: Build multiple itinerary options."""
    clear_screen()
    print_header("🎲 BUILD MULTIPLE ITINERARY OPTIONS")
    
    print("\n   Generate several diversified itinerary options!\n")
    
    city = get_input("   🏙️  City", "Pittsburgh, PA")
    user_address = get_input("   🏠 Your starting address", "Hamburg Hall, 4800 Forbes Ave, Pittsburgh, PA 15213")
    max_distance = get_float_input("   📏 Max distance (miles)", 5.0)
    num_options = get_int_input("   🔢 Number of options", 3)
    environment = get_choice("   🌤️  Environment preference", ["indoor", "outdoor", "either"], "either")
    
    print("\n")
    animate_loading(f"Generating {num_options} unique itinerary options", duration=2.5)
    
    try:
        req = ItineraryRequest(
            city=city,
            user_address=user_address,
            max_distance_miles=max_distance,
            preferences=Preference(environment=environment),
        )
        resp = build_itinerary_options(req)
        print(f"\n✅ Generated {len(resp.options)} options successfully!\n")
        
        for idx, opt in enumerate(resp.options, start=1):
            print(f"\n{'═' * 78}")
            print(f"║{'OPTION ' + str(idx):^76}║")
            print_itinerary(opt.model_dump())
            if idx < len(resp.options):
                input("\n   Press ENTER to see next option...")
    except Exception as e:
        print(f"\n❌ Error building options: {e}")
    
    input("\n\n   Press ENTER to return to main menu...")


def option_search_food() -> None:
    """Menu option: Search for food via Yelp."""
    clear_screen()
    print_header("🍕 SEARCH FOOD (YELP)")
    
    print("\n   Find delicious restaurants in Pittsburgh!\n")
    
    query = get_input("   🔍 Search query (e.g., ramen, pizza)", "ramen")
    location = get_input("   📍 Location", "Pittsburgh, PA")
    limit = get_int_input("   🔢 Number of results", 5)
    price_input = get_input("   💰 Price levels (1,2,3,4 or leave blank)", "")
    price = price_input if price_input else None
    
    print("\n")
    animate_loading("Searching Yelp for amazing food", duration=1.5)
    
    try:
        results = search_food(query=query, location=location, limit=limit, price=price)
        print("\n✅ Search completed!\n")
        print_food_results(results)
    except Exception as e:
        print(f"\n❌ Error searching food: {e}")
    
    input("\n\n   Press ENTER to return to main menu...")


def option_this_week_events() -> None:
    """Menu option: Fetch this week's events from VisitPittsburgh."""
    clear_screen()
    print_header("🎪 THIS WEEK'S EVENTS")
    
    print("\n   Fetching the latest Pittsburgh events...\n")
    animate_loading("Scraping VisitPittsburgh.com", duration=2.0)
    
    try:
        events = fetch_this_week_events()
        print("\n✅ Events retrieved successfully!\n")
        print_events(events)
    except Exception as e:
        print(f"\n❌ Error fetching events: {e}")
    
    input("\n\n   Press ENTER to return to main menu...")


def option_json_export() -> None:
    """Menu option: Build itinerary and export as JSON."""
    clear_screen()
    print_header("💾 BUILD ITINERARY & EXPORT JSON")
    
    print("\n   Generate an itinerary and save it as JSON!\n")
    
    city = get_input("   🏙️  City", "Pittsburgh, PA")
    user_address = get_input("   🏠 Your starting address", "Hamburg Hall, 4800 Forbes Ave, Pittsburgh, PA 15213")
    max_distance = get_float_input("   📏 Max distance (miles)", 5.0)
    filename = get_input("   📄 Output filename", "itinerary.json")
    
    print("\n")
    animate_loading("Building itinerary", duration=2.0)
    
    try:
        req = ItineraryRequest(
            city=city,
            user_address=user_address,
            max_distance_miles=max_distance,
        )
        resp = build_itinerary(req)
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(resp.model_dump(), f, indent=2, default=str)
        
        print(f"\n✅ Itinerary saved to {filename}!\n")
        print_itinerary(resp.model_dump())
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    input("\n\n   Press ENTER to return to main menu...")


# ============================================================================
# MAIN MENU
# ============================================================================

MENU_OPTIONS = """
╔══════════════════════════════════════════════════════════════════════════╗
║                            MAIN MENU                                     ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║   1️⃣   Build Single Weekend Itinerary                                     ║
║   2️⃣   Build Multiple Itinerary Options                                   ║
║   3️⃣   Search Food (Yelp)                                                 ║
║   4️⃣   View This Week's Events                                            ║
║   5️⃣   Build Itinerary & Export JSON                                      ║
║   6️⃣   Exit                                                               ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
"""


def show_menu() -> str:
    """Display main menu and get user choice."""
    clear_screen()
    print(TITLE_ART)
    print(MENU_OPTIONS)
    choice = input("   👉 Select an option (1-6): ").strip()
    return choice


def main_loop() -> None:
    """Main interactive loop."""
    while True:
        choice = show_menu()
        
        if choice == "1":
            option_build_itinerary()
        elif choice == "2":
            option_build_options()
        elif choice == "3":
            option_search_food()
        elif choice == "4":
            option_this_week_events()
        elif choice == "5":
            option_json_export()
        elif choice == "6":
            clear_screen()
            print("\n")
            typewriter("   👋 Thanks for using Weekender! Have a great weekend in Pittsburgh! 🐢\n")
            print("\n")
            sys.exit(0)
        else:
            print("\n   ❌ Invalid choice. Please select 1-6.")
            time.sleep(1.5)


# ============================================================================
# ENTRY POINT
# ============================================================================

def main() -> None:
    """Entry point for interactive CLI."""
    configure_logging()
    _ = get_settings()  # Load config
    
    show_intro()
    main_loop()


if __name__ == "__main__":
    main()
