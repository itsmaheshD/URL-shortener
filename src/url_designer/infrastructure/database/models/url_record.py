from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class UrlRecord(SQLModel, table=True):
    """Persisted representation of a shortened URL."""

    id: int | None = Field(default=None, primary_key=True)

    original_url: str | None = Field(default=None)

    short_code_url: str = Field(
        index=True,
        unique=True
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


