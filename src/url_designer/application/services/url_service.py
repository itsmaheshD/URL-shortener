from sqlmodel import Session

from url_designer.domain.short_code import ShortCode
from url_designer.domain.domain import OriginalUrl
from url_designer.infrastructure.database.models.url_record import UrlRecord
from url_designer.infrastructure.database.repositories.url_repository import (
    URLRepository,
)
from url_designer.infrastructure.redis.cache import RedisCache
from url_designer.infrastructure.redis.keys import url_cache_key
from url_designer.services.short_code_generator import ShortCodeGenerator


class URLService:
    """Application service for URL-shortening operations."""

    def __init__(
        self,
        session: Session,
        repository: URLRepository,
        short_code_generator: ShortCodeGenerator,
        cache: RedisCache,
    ) -> None:
        self._session = session
        self._repository = repository
        self._short_code_generator = short_code_generator
        self._cache = cache

    def create_short_url(self, original_url: str) -> UrlRecord:
        """Create and persist a shortened URL."""

        # Validate the original URL using the domain object.
        validated_url = OriginalUrl(original_url)

        try:
            # Generate a unique public short code before persistence.
            short_code = self._generate_unique_short_code()

            # Validate the generated short code.
            validated_short_code = ShortCode(short_code)

            # Create the complete database record.
            url_record = UrlRecord(
                original_url=validated_url.value,
                short_code_url=validated_short_code.value,
            )

            # Persist the complete record.
            url_record = self._repository.create(url_record)

            # Commit only after successful persistence.
            self._session.commit()

            return url_record

        except Exception:
            # Roll back the database transaction if creation fails.
            self._session.rollback()
            raise

    def get_original_url(self, short_code_url: str) -> str:
        """Return the original URL using Redis before PostgreSQL."""

        # Build the standard Redis cache key.
        cache_key = url_cache_key(short_code_url)

        # Check Redis before querying PostgreSQL.
        cached_url = self._cache.get(cache_key)

        if cached_url is not None:
            return cached_url

        # Redis miss: retrieve the URL from PostgreSQL.
        url_record = self._repository.get_by_short_code(
            short_code_url,
        )

        if url_record is None:
            raise ValueError(
                f"Short URL '{short_code_url}' was not found."
            )

        # Store the database result in Redis for subsequent requests.
        self._cache.set(
            cache_key,
            url_record.original_url,
        )

        return url_record.original_url

    def _generate_unique_short_code(self) -> str:
        """Generate a short code that does not already exist."""

        while True:
            short_code = self._short_code_generator.generate()

            if self._repository.get_by_short_code(short_code) is None:
                return short_code