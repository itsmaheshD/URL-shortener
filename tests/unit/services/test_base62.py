from url_designer.services.base62 import Base62Service

import pytest


def test_encode_zero() -> None:
    service = Base62Service()

    assert service.encode(0) == "0"


def test_encode_known_values() -> None:
    service = Base62Secvice()

    assert service.encode(61) == "z"
    assert service.encode(62) == "10"


def test_decode_knownn_values() -> None:
    service = Base62Service()

    assert service.decode("0") == 0
    assert service.decode("Z") == 61
    assert service.decode("10") == 62


def test_encode_decode_round_trip() -> None:
    service = Base62Service()
    values = [0, 1, 10, 61, 62, 100, 12345, 999999]

    for value in values:
        encoded = service.encode(value)
        assert service.decode(encoded) == value


def test_encode_rejects_negative_number() -> None:
    service = Base62Service()

    with pytest.raises(ValueError, match="non-negative"):
        service.encode(-1)


def test_decode_rejects_empty_value() -> None:
    service = Base62Service()

    with pytest.raises(ValueError, match="cannot be empty"):
        service.decode("")


def test_decode_rejects_invalid_character() -> None:
    service = Base62Service()

    with pytest.raises(ValueError, match="Invalid Base62"):
        service.decode("abc-123")
