from fastapi.testclient import TestClient

from url_designer.main import app


client = TestClient(app)


def test_create_short_url() -> None:
    """Verify that a URL can be shortened through the HTTP API."""

    response = client.post(
        "/urls",
        json={
            "original_url": "https://www.youtube.com/",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] > 0
    assert data["original_url"] == "https://www.youtube.com/"
    assert isinstance(data["short_code_url"], str)
    assert len(data["short_code_url"]) == 6
    assert data["short_code_url"].isalnum()


def test_create_short_url_rejects_invalid_url() -> None:
    """Verify that an invalid URL is rejected by the API."""

    response = client.post(
        "/urls",
        json={
            "original_url": "not-a-valid-url",
        },
    )

    assert response.status_code == 422