from fastapi import APIRouter, Request, BackgroundTasks
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException

from app.core.exceptions import ShortCodeGenerationError, UrlNotFoundError
from app.schemas.url_schema import UrlCreate, ShortUrlResponse, UrlStatsResponse
from app.dependencies.url_dependency import UrlDep
from app.tasks.url_db_task import increment_click_task

router = APIRouter()

@router.post("/shorten", response_model=ShortUrlResponse)
def create_short_url(service: UrlDep, url: UrlCreate, request: Request):
  try:
    url_obj = service.get_or_create(url)

    return ShortUrlResponse(short_url=f"{str(request.base_url).rstrip('/')}/{url_obj.short_code}")
  
  except ShortCodeGenerationError as exc:
    raise HTTPException(status_code=500, detail=str(exc))

@router.get("/{short_code}")
def fetch_long_url(service: UrlDep, short_code: str, background_tasks: BackgroundTasks):
  try:
    url_obj = service.fetch_long_url(short_code)

    background_tasks.add_task(increment_click_task, short_code)

    return RedirectResponse(url=url_obj.long_url)
  
  except UrlNotFoundError:
    raise HTTPException(status_code=404, detail="Short code not found")
  
@router.get("/stats/{short_url:path}", response_model=UrlStatsResponse)
def fetch_stats(service: UrlDep, short_url: str):
  try:
    url_obj = service.fetch_stats(short_url)

    return UrlStatsResponse(click_count=url_obj.click_count)
  
  except UrlNotFoundError:
    raise HTTPException(status_code=404, detail="Short_url not found")