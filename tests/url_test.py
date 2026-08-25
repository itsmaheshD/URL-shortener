import pytest

from url_designer.domain import OriginalUrl


def test_accepts_https_url() -> None:
    url = OriginalUrl("https://example.com")

    assert url.value == "https://example.com"


def test_accepts_http_url() -> None:
    url = OriginalUrl("http://example.com/products")

    assert url.value == "http://example.com/products"


def test_rejects_url_without_scheme() -> None:
    with pytest.raises(ValueError, match="HTTP or HTTPS"):
        OriginalUrl("example.com")


def test_rejects_unsupported_scheme() -> None:
    with pytest.raises(ValueError, match="HTTP or HTTPS"):
        OriginalUrl("ftp://example.com")


