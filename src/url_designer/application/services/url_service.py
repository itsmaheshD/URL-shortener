from sqlmodel import Session

from url_designer.domain.short_code import ShortCode
from url_designer.domain.domain import OriginalUrl
from url_designer.infrastructure.database.models.url_record import UrlRecord
from url_designer.infrastructure.database.repositories.url_repository import (
    URLRepository,
)
from url_designer.services.base62 import Base62Service


class URLService:
    """Application service for URL-shortening operations."""

    def __init__(
        self,
        session: Session,
        repository: URLRepository,
        base62_service: Base62Service,
    ) -> None:
        self._session = session
        self._repository = repository
        self._base62_service = base62_service

    def create_short_url(self, original_url: str) -> UrlRecord:
        """Create and persist a shortened URL atomically."""
        validated_url = OriginalUrl(original_url)

        try:
            # Add the record and obtain its database-generated ID.
            url_record = UrlRecord(
                original_url=validated_url.value,
            )

            url_record = self._repository.create(url_record)

            if url_record.id is None:
                raise RuntimeError(
                    "Database did not generate an identifier."
                )

            # Generate the short code from the database ID.
            encoded_short_code = self._base62_service.encode(url_record.id)

            # Validate the generated short code.
            short_code = ShortCode(encoded_short_code)

            # Update the record inside the same transaction.
            url_record = self._repository.update_short_code(
                url_record,
                short_code.value,
            )

            self._session.commit()

            return url_record

        except Exception:
            self._session.rollback()
            raise