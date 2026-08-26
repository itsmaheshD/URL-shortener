from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parents[4]


class Settings(BaseSettings):
    database_url: str
    test_database_url: str
    """Redis server settings."""
    redis_host: str
    redis_port: int
    redis_db: int
    redis_cache_ttl_seconds: int


    # Resolve the path from this source file instead of the process working
    # directory. This also works when session.py is run from an IDE.
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
    )


settings = Settings()


def get_database_url() -> str:
    return settings.database_url


