import pytest
from unittest.mock import Mock

from fastapi.testclient import TestClient

from app.models.url_model import Url
from app.dependencies.url_dependency import get_url_service
from app.main import app

@pytest.fixture
def mock_service():
  return Mock()

@pytest.fixture
def client(mock_service):
  app.dependency_overrides[get_url_service] = lambda: mock_service

  with TestClient(app) as c:
    yield c
  
  app.dependency_overrides.clear()

@pytest.fixture
def mock_url_obj():
  return Url(
    id=1,
    long_url="https://example.com",
    short_code="xyz123"
  )