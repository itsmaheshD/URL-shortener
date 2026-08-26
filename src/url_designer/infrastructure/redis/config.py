from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisSettings(BaseSettings):
    """Redis connection configuration."""

    host: str = "localhost"
    port: int = 6379
    db: int = 0
    cache_ttl_seconds: int = 3600

    model_config = SettingsConfigDict(
        env_prefix="REDIS_",
        env_file=".env",
        extra="ignore",
    )

    @property
    def redis_url(self) -> str:
        """Build the Redis connection URL."""
        return f"redis://{self.host}:{self.port}/{self.db}"


redis_settings = RedisSettings()