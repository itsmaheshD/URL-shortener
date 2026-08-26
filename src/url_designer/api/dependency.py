from fastapi import Depends
from sqlmodel import Session

from url_designer.application.services.url_service import URLService
from url_designer.infrastructure.database.repositories.url_repository import (
    URLRepository,
)
from url_designer.infrastructure.database.session import get_session
from url_designer.infrastructure.redis.cache import RedisCache
from url_designer.infrastructure.redis.client import get_redis_client
from url_designer.infrastructure.redis.config import redis_settings
from url_designer.services.short_code_generator import ShortCodeGenerator


def get_redis_cache() -> RedisCache:
    """Create the Redis cache for the current request."""

    return RedisCache(
        client=get_redis_client(),
        default_ttl_seconds=redis_settings.cache_ttl_seconds,
    )


def get_url_service(
    session: Session = Depends(get_session),
    cache: RedisCache = Depends(get_redis_cache),
) -> URLService:
    """Create the URL service for the current request."""

    repository = URLRepository(session)
    short_code_generator = ShortCodeGenerator()

    return URLService(
        session=session,
        repository=repository,
        short_code_generator=short_code_generator,
        cache=cache,
    )