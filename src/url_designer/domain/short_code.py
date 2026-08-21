import re
from dataclasses import dataclass

_BASE62_PATTERN = re.compile(r"^[a-zA-Z0-9]+$")


@dataclass(frozen=True)
class ShortCode:
    """Represents a valid URL short code"""

    value: str

    def __post_init__(self) -> None:
        """Validate that the short code contains only Base62 characters."""
        if not self.value:
            raise ValueError("Short code cannot be empty.")

        if not _BASE62_PATTERN.fullmatch(self.value):
            raise ValueError(
                "Short code must contain only letters and digits."
            )
