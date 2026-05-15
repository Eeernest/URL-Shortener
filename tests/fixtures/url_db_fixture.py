import pytest

from app.models.url_model import Url
from app.repositories.url_db_repository import UrlDbRepository
from tests.conftest import db_session

@pytest.fixture
def url_db_repo(db_session):
  return UrlDbRepository(db_session)

@pytest.fixture
def create_url_obj():
  return Url(long_url="https://github.com/", short_code="xyz123")

@pytest.fixture
async def saved_url_obj(url_db_repo, create_url_obj):
  return await url_db_repo.save(create_url_obj)