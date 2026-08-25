from sqlmodel import Session

from url_designer.domain.short_code import ShortCode
from url_designer.domain.domain import OriginalUrl
from url_designer.infrastructure.database.models.url_record import UrlRecord
from url_designer.infrastructure.database.repositories.url_repository import (
    URLRepository,
)
from url_designer.services.short_code_generator import ShortCodeGenerator


class URLService:
    """Application service for URL-shortening operations."""

    def __init__(
        self,
        session: Session,
        repository: URLRepository,
        short_code_generator: ShortCodeGenerator,
    ) -> None:
        self._session = session
        self._repository = repository
        self._short_code_generator = short_code_generator

    def create_short_url(self, original_url: str) -> UrlRecord:
        """Create and persist a shortened URL atomically."""

        validated_url = OriginalUrl(original_url)

        try:
            # Generate a public short code before persistence.
            short_code = self._generate_unique_short_code()

            # Validate the generated value using the domain object.
            validated_short_code = ShortCode(short_code)

            # Create the complete record before inserting it.
            url_record = UrlRecord(
                original_url=validated_url.value,
                short_code_url=validated_short_code.value,
            )

            # Persist the complete record in one database operation.
            url_record = self._repository.create(url_record)

            # Commit only after the complete record has been created.
            self._session.commit()

            return url_record

        except Exception:
            # Roll back the transaction if creation fails.
            self._session.rollback()
            raise

    def get_original_url(self, short_code:str)->str:
        url_record=self._repository.get_by_short_code(
            short_code
        )
        if url_record is None:
            raise ValueError("Valid URL Not Found")

        return url_record.original_url


    def _generate_unique_short_code(self) -> str:
        """Generate a short code that does not already exist."""

        while True:
            short_code = self._short_code_generator.generate()

            if self._repository.get_by_short_code(short_code) is None:
                return short_code