from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass(frozen=True)
class OriginalUrl:
    """Represents a validated original URL in the domain."""

    value: str

    def __post_init__(self) -> None:
        """Validate that the URL uses HTTP/HTTPS and contains a host."""
        parsed_url = urlparse(self.value)

        if parsed_url.scheme not in {"http", "https"}:
            raise ValueError("URL must use HTTP or HTTPS.")

        if not parsed_url.netloc:
            raise ValueError("URL must contain a host.")


