from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException

from app.core.exceptions import ShortCodeGenerationError, UrlNotFoundError
from app.schemas.url_schema import UrlCreate, ShortUrlResponse
from app.dependencies.url_dependency import UrlDep

router = APIRouter()

@router.post("/shorten", response_model=ShortUrlResponse)
def create_short_url(service: UrlDep, url: UrlCreate, request: Request):
  try:
    url_obj = service.get_or_create(url)
    short_url = service.create_short_url(str(request.base_url), url_obj.short_code)

    return ShortUrlResponse(short_url=short_url)
  
  except ShortCodeGenerationError as exc:
    raise HTTPException(status_code=500, detail=str(exc))

@router.get("/{short_code}")
def fetch_long_url(service: UrlDep, short_code: str):
  try:
    return RedirectResponse(url=service.redirect(short_code))
  
  except UrlNotFoundError:
    raise HTTPException(status_code=404, detail="Short code not found")