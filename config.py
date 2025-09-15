"""
Title: App Configuration (Settings)
Team: Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks
CMU IDs: nhicks, aadyaaga, yepeng, wendyl2
Date: 2025-09-15
Summary: Centralized configuration using pydantic BaseSettings. Loads from environment.
Disclaimer: This file includes AI-assisted content (GPT-5); reviewed and approved by the Purple Turtles team.
"""

from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field("weekender", validation_alias="APP_NAME")
    env: str = Field("development", validation_alias="ENV")
    debug: bool = Field(True, validation_alias="DEBUG")
    log_level: str = Field("INFO", validation_alias="LOG_LEVEL")
    port: int = Field(8000, validation_alias="PORT")

    openai_api_key: str = Field("changeme-openai-key", validation_alias="OPENAI_API_KEY")
    openai_model: str = Field("gpt-5-nano", validation_alias="OPENAI_MODEL")
    openai_max_completion_tokens: int = Field(500, validation_alias="OPENAI_MAX_COMPLETION_TOKENS")
    openai_concurrency: int = Field(8, validation_alias="OPENAI_CONCURRENCY")
    maps_api_key: str = Field("changeme-maps-key", validation_alias="MAPS_API_KEY")
    weather_api_key: str = Field("changeme-weather-key", validation_alias="WEATHER_API_KEY")
    events_api_key: str = Field("changeme-events-key", validation_alias="EVENTS_API_KEY")
    yelp_api_key: str = Field("changeme-yelp-key", validation_alias="YELP_API_KEY")
    ticketmaster_api_key: str = Field("changeme-ticketmaster-key", validation_alias="TICKETMASTER_API_KEY")

    # Maps provider selection: "google" or "none" (haversine fallback)
    maps_provider: str = Field("google", validation_alias="MAPS_PROVIDER")

    cache_backend: str = Field("memory", validation_alias="CACHE_BACKEND")
    database_url: str = Field("sqlite:///./weekender.sqlite3", validation_alias="DATABASE_URL")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]


