"""Application configuration."""

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Load environment-backed application settings."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    openai_api_key: str = Field(default="", validation_alias="OPENAI_API_KEY")
    openai_model: str = Field(default="", validation_alias="OPENAI_MODEL")
    openai_embedding_model: str = Field(
        default="text-embedding-3-small", validation_alias="OPENAI_EMBEDDING_MODEL"
    )
    jolpica_base_url: str = Field(
        default="https://api.jolpi.ca/ergast/f1", validation_alias="JOLPICA_BASE_URL"
    )
    f1_start_season: int = Field(default=2020, validation_alias="F1_START_SEASON")
    f1_end_season: str = Field(default="current", validation_alias="F1_END_SEASON")
    chroma_path: Path = Field(default=Path("data/vector_store"), validation_alias="CHROMA_PATH")
    log_level: str = Field(default="INFO", validation_alias="LOG_LEVEL")


@lru_cache
def get_settings() -> Settings:
    """Return the cached application settings."""

    # Cache the parsed settings; changes to .env require a restart or cache reset.
    return Settings()
