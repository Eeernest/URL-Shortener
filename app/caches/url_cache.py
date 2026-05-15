from typing import Annotated

from fastapi import Depends
from redis.asyncio import Redis, ConnectionPool

from app.core.config import Config

pool = ConnectionPool.from_url(Config.CACHE_URL, decode_responses=True)

async def get_redis():
  client = Redis.from_pool(pool, protocol=3)

  try:
    yield client
  finally:
    await client.close()

RedisDep = Annotated[Redis, Depends(get_redis)]