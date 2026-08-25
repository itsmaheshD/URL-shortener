from fastapi import Depends
from sqlmodel import Session

from url_designer.application.services.url_service import URLService
from url_designer.infrastructure.database.repositories.url_repository import (
    URLRepository,
)
from url_designer.infrastructure.database.session import get_session
from url_designer.services.short_code_generator import ShortCodeGenerator


def get_url_service(
    session: Session = Depends(get_session),
) -> URLService:
    """Create the URL service for the current request."""

    repository = URLRepository(session)
    short_code_generator = ShortCodeGenerator()

    return URLService(
        session=session,
        repository=repository,
        short_code_generator=short_code_generator,
    )