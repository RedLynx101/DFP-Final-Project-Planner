"""
Title: Logging Configuration
Team: Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks
Date: 2025-09-11
Summary: Structured logging setup.
Disclaimer: This file includes AI-assisted content (GPT-5); reviewed and approved by the Purple Turtles team.
"""

import logging
import sys
from .config import get_settings


def configure_logging() -> None:
    settings = get_settings()
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        stream=sys.stdout,
    )


