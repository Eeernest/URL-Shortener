from tests.db.url_db import db_session
from tests.fixtures.url_fixture import url_db_repo, create_url_obj, saved_url_obj

def test_get_long_url(url_db_repo, saved_url_obj):
  result = url_db_repo.get_long_url(saved_url_obj.long_url)

  assert result.id is not None
  assert result.long_url == saved_url_obj.long_url
  assert result.short_code == saved_url_obj.short_code

def test_save(url_db_repo, create_url_obj):
  result = url_db_repo.save(create_url_obj)

  assert result.id is not None
  assert result.long_url == create_url_obj.long_url
  assert result.short_code == create_url_obj.short_code