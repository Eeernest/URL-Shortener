from pydantic import BaseModel, HttpUrl
from datetime import datetime

class UrlCreate(BaseModel):
  long_url: HttpUrl


class ShortUrlResponse(BaseModel):
  short_url: HttpUrl