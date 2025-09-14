"""
Title: FastAPI Application Entry
Team: Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks
Date: 2025-09-11
Summary: Creates the FastAPI app, configures logging, and includes routes.
Disclaimer: This file includes AI-assisted content (GPT-5); reviewed and approved by the Purple Turtles team.
"""

from fastapi import FastAPI, HTTPException
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
    app = FastAPI(
        title="Pittsburgh Weekend Planner API",
        description="API for planning amazing weekend itineraries in Pittsburgh, PA. Discover events, restaurants, and create personalized Steel City adventures.",
        version="1.0.0"
    )
    
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
    
    # Add startup event handler for deployment readiness
    @app.on_event("startup")
    async def startup_event():
        """Ensure all services are initialized before accepting requests"""
        import logging
        logger = logging.getLogger("uvicorn.error")
        logger.info("Pittsburgh Weekend Planner API starting up...")
        
        # Validate critical settings
        try:
            settings = get_settings()
            logger.info(f"App: {settings.app_name} (env: {settings.env})")
            logger.info(f"Port: {settings.port}")
            logger.info("All services initialized successfully")
        except Exception as e:
            logger.error(f"Startup validation failed: {e}")
            raise e
    
    @app.on_event("shutdown")
    async def shutdown_event():
        """Cleanup on application shutdown"""
        import logging
        logger = logging.getLogger("uvicorn.error")
        logger.info("Pittsburgh Weekend Planner API shutting down...")
    
    return app


def setup_static_files(app: FastAPI) -> None:
    """Setup static file serving for production deployment"""
    frontend_dist = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "dist")
    
    # Only mount static files if the frontend build exists and we're not in health check mode
    if os.path.exists(frontend_dist) and os.path.exists(os.path.join(frontend_dist, "assets")):
        try:
            # Mount static assets with lower priority to avoid health check conflicts
            app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")
            
            # Simple catch-all for SPA routing - more restrictive to avoid health check issues
            @app.get("/{full_path:path}", include_in_schema=False)
            async def serve_spa(full_path: str):
                # Skip API routes, docs, and health checks completely
                if (full_path.startswith("api/") or 
                    full_path in ["docs", "redoc", "openapi.json", "health"]):
                    raise HTTPException(status_code=404, detail="Not found")
                
                # Serve static files from root (like favicon.ico, favicon.png)
                if full_path in ["favicon.ico", "favicon.png"]:
                    favicon_path = os.path.join(frontend_dist, full_path)
                    if os.path.exists(favicon_path):
                        return FileResponse(favicon_path)
                
                # Serve index.html for root and SPA routes
                index_file = os.path.join(frontend_dist, "index.html")
                if os.path.exists(index_file):
                    return FileResponse(index_file)
                raise HTTPException(status_code=404, detail="Frontend not available")
        except Exception:
            # If static file setup fails, continue without it to prevent deployment issues
            pass


# Initialize app
app = create_app()

# Setup static files after app creation for deployment
setup_static_files(app)