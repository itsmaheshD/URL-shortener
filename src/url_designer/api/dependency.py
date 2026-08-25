from fastapi import Depends
from sqlmodel import Session
from url_designer.application.services.url_service import URLService
from url_designer.infrastructure.database.repositories.url_repository import URLRepository

from url_designer.infrastructure.database.session import get_session
from url_designer.services.base62 import Base62Service

def get_url_service(
        session: Session=Depends(get_session)
        )->URLService:
    repository = URLRepository(session)
    base62_service = Base62Service()


    return URLService(
        session=session,
        repository=repository,
        base62_service=base62_service
    )