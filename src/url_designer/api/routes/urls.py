from fastapi import APIRouter, Depends, status
from fastapi.responses import RedirectResponse

from url_designer.api.dependency import get_url_service
from url_designer.api.schemas.url import (
    CreateURLRequest,
    CreateURLResponse,
)
from url_designer.application.services.url_service import URLService


router = APIRouter(

)


@router.post(
    "/url",
    response_model=CreateURLResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_short_url(
    request: CreateURLRequest,
    service: URLService = Depends(get_url_service),
) -> CreateURLResponse:
    """Create a shortened URL."""

    result = service.create_short_url(
        str(request.original_url),
    )

    if result.id is None:
        raise RuntimeError("URL record was not assigned an identifier.")

    return CreateURLResponse(
        id=result.id,
        original_url=result.original_url or "",
        short_code_url=result.short_code_url or "",
    )

@router.get(
    "/{short_code_url}",
    status_code=302,
)
def redirect_to_original_url(
    short_code_url: str,
    service: URLService = Depends(get_url_service),
) -> RedirectResponse:
    """Redirect a short URL to its original URL."""

    original_url = service.get_original_url(
        short_code_url,
    )

    return RedirectResponse(
        url=original_url,
        status_code=302,
    )