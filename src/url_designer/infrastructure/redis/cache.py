from redis import Redis
from redis.exceptions import RedisError


class RedisCache:
    """Provide resilient key-value cache operations using Redis."""

    def __init__(
        self,
        client: Redis,
        default_ttl_seconds: int = 3600,
    ) -> None:
        self._client = client
        self._default_ttl_seconds = default_ttl_seconds

    def get(self, key: str) -> str | None:
        """Get a cached value, returning None if Redis is unavailable."""

        try:
            return self._client.get(key)

        except RedisError as errors_get_key:
            # Redis is a cache, so reads continue through PostgreSQL.
            print("The redis get key error's", errors_get_key)
            return None

    def set(
        self,
        key: str,
        value: str,
        expiration_seconds: int | None = None,
    ) -> None:
        """Store a value in Redis with a configurable TTL."""

        try:
            ttl = (
                expiration_seconds
                if expiration_seconds is not None
                else self._default_ttl_seconds
            )

            self._client.set(
                name=key,
                value=value,
                ex=ttl,
            )
        except RedisError as errors_set_key:
            # Cache failures must not break the application.
            print("The redis set key error is ",errors_set_key)
            pass

    def delete(self, key: str) -> None:
        """Delete a cached value without breaking the application."""

        try:
            self._client.delete(key)
        except RedisError:
            # Cache deletion failure is non-critical.
            pass