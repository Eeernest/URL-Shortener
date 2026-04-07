from fastapi import APIRouter, Request, BackgroundTasks, HTTPException
from fastapi.responses import RedirectResponse

from app.core.middleware import limiter
from app.dependencies.url_dependency import UrlDep
from app.schemas.url_schema import UrlCreate, ShortUrlResponse, UrlStatsResponse
from app.tasks.url_db_task import increment_click_task

router = APIRouter()

@router.post("/shorten", response_model=ShortUrlResponse)
@limiter.limit("10/minute")
def create_short_url(service: UrlDep, url: UrlCreate, request: Request):
  url_obj = service.get_or_create(url)

  return ShortUrlResponse(short_url=f"{str(request.base_url).rstrip('/')}/{url_obj.short_code}")

@router.get("/{short_code}")
@limiter.limit("100/minute")
def fetch_long_url(service: UrlDep, short_code: str, background_tasks: BackgroundTasks, request: Request):
  url_obj = service.fetch_long_url(short_code)

  background_tasks.add_task(increment_click_task, short_code)

  return RedirectResponse(url=url_obj.long_url)
  
@router.get("/stats/{short_url:path}", response_model=UrlStatsResponse)
@limiter.limit("10/minute")
def fetch_stats(service: UrlDep, short_url: str, request: Request):
  url_obj = service.fetch_stats(short_url)

  return UrlStatsResponse(click_count=url_obj.click_count)