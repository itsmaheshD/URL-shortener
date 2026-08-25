from pydantic import BaseModel, HttpUrl


class CreateURLRequest(BaseModel):
    """Request payload for creating a shortened URL."""

    original_url: HttpUrl


class CreateURLResponse(BaseModel):
    """Response returned after creating a shortened URL."""

    id: int
    original_url: str
    short_code_url: str