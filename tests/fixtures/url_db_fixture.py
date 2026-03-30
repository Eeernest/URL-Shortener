import pytest
from unittest.mock import Mock

from app.models.url_model import Url
from app.repositories.url_db_repository import UrlDbRepository
from app.services.url_service import UrlService

from tests.db.url_db import db_session

@pytest.fixture
def url_db_repo(db_session):
  return UrlDbRepository(db_session)

@pytest.fixture
def create_url_obj():
  return Url(long_url="https://github.com/", short_code="xyz123")

@pytest.fixture
def saved_url_obj(url_db_repo, create_url_obj):
  return url_db_repo.save(create_url_obj)

@pytest.fixture
def mock_url_obj():
  return Url(
    id=1,
    long_url="https://github.com/",
    short_code="xyz123"
  )

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