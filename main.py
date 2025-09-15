"""
Title: FastAPI Application Entry (Flat Layout)
Team: Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks
CMU IDs: nhicks, aadyaaga, yepeng, wendyl2
Date: 2025-09-15
Summary: Creates the FastAPI app, configures logging, and includes routes. Flat layout.
Disclaimer: This file includes AI-assisted content (GPT-5); reviewed and approved by the Purple Turtles team.
"""

from fastapi import FastAPI
from config import get_settings
from logging_config import configure_logging
from routes import router as api_router


def create_app() -> FastAPI:
    configure_logging()
    settings = get_settings()
    app = FastAPI(title=settings.app_name)
    app.include_router(api_router, prefix="/api")
    return app


app = create_app()


