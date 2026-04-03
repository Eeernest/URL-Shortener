from tests.conftest import db_session
from tests.fixtures.url_db_fixture import url_db_repo, create_url_obj, saved_url_obj

def test_get_by_long_url(url_db_repo, saved_url_obj):
  result = url_db_repo.get_by_long_url(saved_url_obj.long_url)

  assert result.id is not None
  assert result.long_url == saved_url_obj.long_url
  assert result.short_code == saved_url_obj.short_code

def test_get_by_short_code(url_db_repo, saved_url_obj):
  result = url_db_repo.get_by_short_code(saved_url_obj.short_code)

  assert result.id is not None
  assert result.long_url == saved_url_obj.long_url
  assert result.short_code == saved_url_obj.short_code

def test_save(url_db_repo, create_url_obj):
  result = url_db_repo.save(create_url_obj)

  assert result.id is not None
  assert result.long_url == create_url_obj.long_url
  assert result.short_code == create_url_obj.short_code

def test_increment_click(url_db_repo, db_session, saved_url_obj):
  url_db_repo.increment_click(saved_url_obj.short_code)

  db_session.refresh(saved_url_obj)

  assert saved_url_obj.click_count == 1