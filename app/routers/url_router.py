from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from app.schemas.url_schema import UrlCreate, ShortUrlResponse
from app.dependencies.url_dependency import UrlDep

router = APIRouter()

@router.post("/shorten", response_model=ShortUrlResponse)
def create_short_url(service: UrlDep, url: UrlCreate, request: Request):
  url_obj = service.get_or_create(url)
  short_url = service.create_short_url(str(request.base_url), url_obj.short_code)

  return ShortUrlResponse(short_url=short_url)

@router.get("/{short_code}")
def redirect(service: UrlDep, short_code: str):
  return RedirectResponse(url=service.redirect(short_code))  