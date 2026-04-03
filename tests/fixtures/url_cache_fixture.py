import pytest

from app.core.config import Config
from app.models.url_model import Url
from app.repositories.url_cache_repository import UrlCacheRepository

@pytest.fixture
def url_cache_repo(redis_container):
  config = Config()
  repo = UrlCacheRepository(redis=redis_container, config=config)

  yield repo

@pytest.fixture
def create_url_obj():
  return Url(long_url="https://github.com/", short_code="xyz123")

@pytest.fixture
def saved_url_obj(url_cache_repo, create_url_obj):
  url_cache_repo.set_url_obj(create_url_obj)
  return create_url_obj