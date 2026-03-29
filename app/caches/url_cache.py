from redis import Redis

from typing import Annotated
from fastapi import Depends

from app.core.config import Config

REDIS_URL = Config.REDIS_URL

redis_client = Redis.from_url(REDIS_URL, decode_responses=True)

def get_redis():
  try:
    yield redis_client

  finally:
    pass

RedisDep = Annotated[Redis, Depends(get_redis)]