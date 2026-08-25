import pytest

from url_designer.application.services.url_service import URLService
from url_designer.infrastructure.database.models.url_record import UrlRecord
from url_designer.services.base62 import Base62Service


class FakeURLRepository:
    """In-memory repository used to test the application service."""

    def __init__(self) -> None:
        self.records: list[UrlRecord] = []
        self.next_id = 1

    def create(self, url_record: UrlRecord) -> UrlRecord:
        """Simulate database persistence and ID generation."""
        url_record.id = self.next_id
        self.next_id += 1

        self.records.append(url_record)

        return url_record

    def update_short_code(
        self,
        url_record: UrlRecord,
        short_code: str,
    ) -> UrlRecord:
        """Simulate updating the short code."""
        url_record.short_code_url = short_code

        return url_record


class FakeSession:
    """Track transaction operations without a database."""

    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass


def test_create_short_url() -> None:
    """Verify the complete URL-shortening workflow."""
    repository = FakeURLRepository()
    base62_service = Base62Service()

    service = URLService(
        session=FakeSession(),
        repository=repository,
        base62_service=base62_service,
    )

    result = service.create_short_url("https://example.com")

    assert result.id == 1
    assert result.original_url == "https://example.com"
    assert result.short_code_url == "1"


def test_create_short_url_rejects_invalid_url() -> None:
    """Verify invalid URLs are rejected before persistence."""
    repository = FakeURLRepository()
    base62_service = Base62Service()

    service = URLService(
        session=FakeSession(),
        repository=repository,
        base62_service=base62_service,
    )

    with pytest.raises(ValueError, match="URL must use HTTP or HTTPS."):
        service.create_short_url("not-a-url")

    assert repository.records == []
