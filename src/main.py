"""
Title: FastAPI Application Entry
Team: Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks
Date: 2025-09-11
Summary: Creates the FastAPI app, configures logging, and includes routes.
Disclaimer: This file includes AI-assisted content (GPT-5); reviewed and approved by the Purple Turtles team.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .core.config import get_settings
from .core.logging_config import configure_logging
from .api.routes import router as api_router
import os


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
        allow_origins=explicit_origins if explicit_origins else ["*"],
        allow_origin_regex=allow_origin_regex,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )
    
    app.include_router(api_router, prefix="/api")
    
    # Serve static files from React build
    frontend_dist = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "dist")
    if os.path.exists(frontend_dist):
        # Mount static assets
        app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")
        
        # Catch-all route for SPA - serves index.html for any non-API route
        @app.get("/{full_path:path}")
        async def serve_spa(full_path: str):
            # Don't interfere with API routes or docs
            if full_path.startswith("api/") or full_path in ["docs", "redoc", "openapi.json"]:
                return {"detail": "Not found"}
            
            # Serve index.html for SPA routing
            index_file = os.path.join(frontend_dist, "index.html")
            if os.path.exists(index_file):
                return FileResponse(index_file)
            else:
                return {"detail": "Frontend not built"}
    
    return app


app = create_app()


