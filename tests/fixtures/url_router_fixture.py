from unittest.mock import Mock

from fastapi.testclient import TestClient
import pytest

from app.dependencies.url_dependency import get_url_service
from app.main import app
from app.models.url_model import Url

@pytest.fixture
def mock_url_service():
  return Mock()

@pytest.fixture
def client(mock_url_service):
  app.dependency_overrides[get_url_service] = lambda: mock_url_service

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