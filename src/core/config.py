"""
Title: App Configuration (Settings)
Team: Purple Turtles — Gwen Li, Aadya Agarwal, Emma Peng, Noah Hicks
Date: 2025-09-11
Summary: Centralized configuration using pydantic BaseSettings. Loads from environment.
Disclaimer: This file includes AI-assisted content (GPT-5); reviewed and approved by the Purple Turtles team.
"""

from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field("weekender", env="APP_NAME")
    env: str = Field("development", env="ENV")
    debug: bool = Field(True, env="DEBUG")
    log_level: str = Field("INFO", env="LOG_LEVEL")
    port: int = Field(8000, env="PORT")

    openai_api_key: str = Field("changeme-openai-key", env="OPENAI_API_KEY")
    maps_api_key: str = Field("changeme-maps-key", env="MAPS_API_KEY")
    weather_api_key: str = Field("changeme-weather-key", env="WEATHER_API_KEY")
    events_api_key: str = Field("changeme-events-key", env="EVENTS_API_KEY")
    yelp_api_key: str = Field("changeme-yelp-key", env="YELP_API_KEY")

    cache_backend: str = Field("memory", env="CACHE_BACKEND")
    database_url: str = Field("sqlite:///./weekender.sqlite3", env="DATABASE_URL")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]


