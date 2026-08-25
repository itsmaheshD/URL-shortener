from fastapi import APIRouter, Depends, status, HTTPException
from url_designer.api.dependency import get_url_service

from url_designer.api.schemas.url import (
         CreateRequest,
         CreateResponse
)
from url_designer.application.services.url_service import URLService

router = APIRouter(
    prefix="/url",
    tags=["Url Designer"],
)

@router.post(
    "",
    response_model=CreateResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_url(
        url_service: URLService = Depends(get_url_service),
        request: CreateRequest = Depends(CreateRequest),
)->CreateResponse:
    """creating short url"""
    result= url_service.create_short_url(
        str(
            request.original_url
        )
    )
    if result.id is None or result.short_code_url is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return  CreateResponse(
        id=result.id,
        short_code=result.short_code_url,
        original_url=result.original_url
    )
