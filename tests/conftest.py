import pytest
from testcontainers.redis import RedisContainer
import redis

from app.core.config import Config
from app.repositories.url_cache_repository import UrlCacheRepository

@pytest.fixture(scope="session")
def redis_container():
  with RedisContainer("redis:7") as rdc:
    client = redis.Redis(
      host=rdc.get_container_host_ip(),
      port=rdc.get_exposed_port(6379),
      decode_responses=True
    )

    yield client