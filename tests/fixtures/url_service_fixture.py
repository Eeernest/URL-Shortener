import pytest
from unittest.mock import Mock

from app.models.url_model import Url
from app.services.url_service import UrlService

@pytest.fixture
def mock_url_obj():
  return Url(
    id=1,
    long_url="https://github.com/",
    short_code="xyz123"
  )

@pytest.fixture
def create_url_obj():
  return Url(long_url="https://github.com/", short_code="xyz123")

@pytest.fixture
def mock_base_url():
  return "http://127.0.0.1:8000/"

@pytest.fixture
def mock_db_repo():
  return Mock()

@pytest.fixture
def mock_cache_repo():
  return Mock()

@pytest.fixture
def url_service(mock_db_repo, mock_cache_repo):
  return UrlService(mock_db_repo, mock_cache_repo)