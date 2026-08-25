from sqlmodel import Session, select

from url_designer.infrastructure.database.models.url_record import UrlRecord


class URLRepository:
    """Persistence operations for URL records."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, url_record: UrlRecord) -> UrlRecord:
        """Add a URL record to the current transaction."""
        self._session.add(url_record)
        self._session.flush()
        self._session.refresh(url_record)

        return url_record

    def update_short_code(
        self,
        url_record: UrlRecord,
        short_code: str,
    ) -> UrlRecord:
        """Update the short code in the current transaction."""
        url_record.short_code_url = short_code
        self._session.flush()

        return url_record

    def get_by_short_code(self, short_code: str) -> UrlRecord | None:
        """Find a URL record by its short code."""
        statement = select(UrlRecord).where(
            UrlRecord.short_code_url == short_code
        )

        return self._session.scalars(statement).first()
