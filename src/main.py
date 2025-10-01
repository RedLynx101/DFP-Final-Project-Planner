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
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os


def create_app() -> FastAPI:
    configure_logging()
    settings = get_settings()
    app = FastAPI(title=settings.app_name)

    # Register existing API routes
    app.include_router(api_router, prefix="/api")

    # Configure template directory (one level above src)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

    # Add homepage route
    @app.get("/", response_class=HTMLResponse)
    async def read_root(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})

    return app


app = create_app()
