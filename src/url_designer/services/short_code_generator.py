import secrets
import string


class ShortCodeGenerator:
    """Generate cryptographically strong random Base62 short codes."""

    _ALPHABET = (
        string.ascii_uppercase
        + string.ascii_lowercase
        + string.digits
    )

    def __init__(self, length: int = 6) -> None:
        """Initialize the generator with the desired code length."""
        if length <= 0:
            raise ValueError("Short code length must be positive.")

        self._length = length

    def generate(self) -> str:
        """Generate a random Base62 short code."""
        return "".join(
            secrets.choice(self._ALPHABET)
            for _ in range(self._length)
        )