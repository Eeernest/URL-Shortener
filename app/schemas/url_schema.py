from pydantic import BaseModel, HttpUrl

class UrlCreate(BaseModel):
  long_url: HttpUrl

class ShortUrlResponse(BaseModel):
  short_url: HttpUrl

class UrlStatsResponse(BaseModel):
  click_count: int