import json

from redis.asyncio import Redis

from app.core.config import Config
from app.models.url_model import Url

class UrlCacheRepository:
  def __init__(self, redis: Redis, config: Config):
    self.redis = redis
    self.config = config

  async def get_by_short_code(self, short_code: str) -> Url | None:
    data = await self.redis.get(short_code)

    if data is not None:
      data_dict = json.loads(data)
      
      return Url(**data_dict)
    
    return None
  
  async def set_url_obj(self, url_obj: Url):
    data = json.dumps({
      "long_url": str(url_obj.long_url),
      "short_code": url_obj.short_code,
    })

    cache_key = url_obj.short_code

    return await self.redis.set(cache_key, data, ex=self.config.TTL)