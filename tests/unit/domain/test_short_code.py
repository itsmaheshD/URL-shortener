import pytest

from url_designer.domain.short_code import ShortCode


def test_accepts_alphanumeric_short_code() -> None:
    short_code = ShortCode("aZ91x")

    assert short_code.value == "aZ91x"


def test_accepts_numeric_short_code() -> None:
    short_code = ShortCode("123456")

    assert short_code.value == "123456"


def test_rejects_empty_short_code() -> None:
    with pytest.raises(ValueError, match="cannot be empty"):
        ShortCode("")


def test_rejects_special_characters() -> None:
    with pytest.raises(ValueError, match="letters and digits"):
        ShortCode("abc-123")


def test_rejects_spaces() -> None:
    with pytest.raises(ValueError, match="letters and digits"):
        ShortCode("abc 123")
