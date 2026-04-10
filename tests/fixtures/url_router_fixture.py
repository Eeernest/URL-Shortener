from unittest.mock import Mock

from fastapi.testclient import TestClient
import pytest

from app.core.config import Config
from app.dependencies.url_dependency import get_url_service
from app.dependencies.workers_dependency import get_url_worker
from app.main import app
from app.models.url_model import Url
from app.repositories.url_db_repository import UrlDbRepository
from app.repositories.url_cache_repository import UrlCacheRepository
from app.services.url_service import UrlService
from app.workers.url_worker import UrlWorker
from tests.conftest import db_session

@pytest.fixture
def mock_url_service():
  return Mock()

@pytest.fixture
def mock_url_worker():
  return Mock()

@pytest.fixture
def mock_client(mock_url_service, mock_url_worker):
  app.dependency_overrides[get_url_service] = lambda: mock_url_service
  app.dependency_overrides[get_url_worker] = lambda: mock_url_worker

  with TestClient(app) as c:
    yield c
  
  app.dependency_overrides.clear()

@pytest.fixture
def mock_url_obj():
  return Url(
    id=1,
    long_url="https://example.com",
    short_code="xyz123",
    click_count=12
  )

@pytest.fixture
def mock_short_url():
  return "http://127.0.0.1:8000/xyz123"

@pytest.fixture
def integration_service(db_session, redis_container):
  config = Config()

  db_repo = UrlDbRepository(db_session)
  cache_repo = UrlCacheRepository(redis_container, config)

  return UrlService(db_repo, cache_repo)

@pytest.fixture
def integration_url_worker(db_session):
  return UrlWorker(lambda: db_session)

@pytest.fixture
def integration_client(integration_service, integration_url_worker):
  app.dependency_overrides[get_url_service] = lambda: integration_service
  app.dependency_overrides[get_url_worker] = lambda: integration_url_worker

  with TestClient(app) as c:
    yield c
  
  app.dependency_overrides.clear()

@pytest.fixture
def payload_long_url():
  return {"long_url": "https://example.com/"}