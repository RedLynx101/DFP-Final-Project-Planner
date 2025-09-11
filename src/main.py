"""
Title: FastAPI Application Entry
Team: Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks
Date: 2025-09-11
Summary: Creates the FastAPI app, configures logging, and includes routes.
Disclaimer: This file includes AI-assisted content (GPT-5); reviewed and approved by the Purple Turtles team.
"""

from fastapi import FastAPI
from .core.config import get_settings
from .core.logging_config import configure_logging
from .api.routes import router as api_router


def create_app() -> FastAPI:
    configure_logging()
    settings = get_settings()
    app = FastAPI(title=settings.app_name)
    app.include_router(api_router, prefix="/api")
    return app


app = create_app()


