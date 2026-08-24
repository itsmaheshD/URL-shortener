from sqlmodel import Session

from url_designer.infrastructure.database.models.url_record import UrlRecord


class URLRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, url_record: UrlRecord) -> UrlRecord:
        """Persist a URL record and return it with its generated identifier."""
        self._session.add(url_record)
        self._session.commit()
        self._session.refresh(url_record)
        return url_record
