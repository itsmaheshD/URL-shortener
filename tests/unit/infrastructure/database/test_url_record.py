from datetime import timezone

from url_designer.infrastructure.database.models.url_record import UrlRecord


def test_url_record_uses_an_aware_utc_timestamp() -> None:
    record = UrlRecord(short_code_url="abc123")

    assert record.created_at.tzinfo is timezone.utc
