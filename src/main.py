"""
Title: FastAPI Application Entry
Team: Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks
Date: 2025-09-11
Summary: Creates the FastAPI app, configures logging, and includes routes.
Disclaimer: This file includes AI-assisted content (GPT-5); reviewed and approved by the Purple Turtles team.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import get_settings
from .core.logging_config import configure_logging
from .api.routes import router as api_router


def create_app() -> FastAPI:
    configure_logging()
    settings = get_settings()
    app = FastAPI(title=settings.app_name)
    
    # Configure CORS with environment-based origins
    cors_origins = settings.cors_origins.split(",")
    
    # Separate explicit origins from regex patterns
    explicit_origins = []
    regex_patterns = []
    
    for origin in cors_origins:
        if '*' in origin:
            # Convert wildcard to regex pattern
            if 'replit.dev' in origin:
                regex_patterns.append(r"^https://.*\.replit\.dev$")
            elif 'repl.co' in origin:
                regex_patterns.append(r"^https://.*\.repl\.co$")
        else:
            explicit_origins.append(origin)
    
    # Combine all regex patterns
    allow_origin_regex = None
    if regex_patterns:
        allow_origin_regex = "|".join(regex_patterns)
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=explicit_origins if explicit_origins else None,
        allow_origin_regex=allow_origin_regex,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )
    
    app.include_router(api_router, prefix="/api")
    return app


app = create_app()


