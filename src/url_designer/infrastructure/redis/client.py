import redis

from url_designer.infrastructure.redis.config import redis_settings


def get_redis_client() -> redis.Redis:
    """Create a Redis client."""
    return redis.Redis.from_url(
        redis_settings.redis_url,
        decode_responses=True,
    )