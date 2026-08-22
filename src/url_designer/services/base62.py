from string import ascii_uppercase, ascii_lowercase, digits



class Base62Service:
    """Encode and decode non-negative integers using Base62."""

    _ALPHABET = digits + ascii_uppercase + ascii_lowercase
    _BASE = len(_ALPHABET)

    def encode(self, number: int) -> str:
        """Encode a non-negative integer as a Base62 string."""
        if number < 0:
            raise ValueError("Number must be non-negative.")

        if number == 0:
            return "0"

        encoded = []

        while number > 0:
            number, remainder = divmod(number, self._BASE)
            encoded.append(self._ALPHABET[remainder])

        return "".join(reversed(encoded))

    def decode(self, value: str) -> int:
        """Decode a Base62 string into a non-negative integer."""
        if not value:
            raise ValueError("Base62 value cannot be empty.")

        number = 0

        for character in value:
            if character not in self._ALPHABET:
                raise ValueError(fInvalid Base62 character: {character!r}")

            number = number * self._BASE + self._ALPHABET.index(character)

        return number
