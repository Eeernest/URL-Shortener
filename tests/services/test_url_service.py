import pytest
from fastapi.exceptions import HTTPException

from sqlalchemy.exc import IntegrityError

from tests.fixtures.url_service_fixture import mock_url_obj, create_url_obj, mock_base_url, mock_db_repo, mock_cache_repo, url_service

def test_get_or_create_get_success(mock_db_repo, mock_url_obj, create_url_obj, url_service):
  mock_db_repo.get_by_long_url.return_value = mock_url_obj

  result = url_service.get_or_create(create_url_obj)

  assert result.id is not None
  assert result.long_url == mock_url_obj.long_url
  assert result.short_code == mock_url_obj.short_code
  assert mock_db_repo.get_by_long_url.assert_called_once
  assert mock_db_repo.save.assert_not_called

def test_get_or_create_create_success(mock_db_repo, mock_url_obj, create_url_obj, url_service):
  mock_db_repo.get_by_long_url.return_value = None
  mock_db_repo.save.return_value = mock_url_obj

  result = url_service.get_or_create(create_url_obj)

  assert result.id is not None
  assert result.long_url == mock_url_obj.long_url
  assert result.short_code == mock_url_obj.short_code
  assert mock_db_repo.get_by_long_url.assert_called_once
  assert mock_db_repo.save.assert_called_once

def test_get_or_create_race_condition(mock_db_repo, mock_url_obj, create_url_obj, url_service):
  mock_db_repo.get_by_long_url.return_value = None
  mock_db_repo.save.side_effect = [IntegrityError("stmt", "params", "orig"), mock_url_obj]

  result = url_service.get_or_create(create_url_obj)

  assert result.id is not None
  assert mock_db_repo.get_by_long_url.assert_called_once
  assert mock_db_repo.save.call_count == 2

def test_get_or_create_race_condition_fail(mock_db_repo, create_url_obj, url_service):
  mock_db_repo.get_by_long_url.return_value = None
  mock_db_repo.save.side_effect = IntegrityError("stmt", "params", "orig")

  with pytest.raises(RuntimeError) as exc:
    url_service.get_or_create(create_url_obj)

  assert "Failed to generate a unique short_code after several attempts" in str(exc.value)
  assert mock_db_repo.get_by_long_url.assert_called_once
  assert mock_db_repo.save.call_count == 5

def test_create_short_url_success(url_service, mock_base_url, mock_url_obj):
  result = url_service.create_short_url(mock_base_url, mock_url_obj.short_code)

  assert result == mock_base_url + mock_url_obj.short_code

def test_redirect_in_cache(mock_cache_repo, mock_url_obj, url_service):
  mock_cache_repo.get_by_short_code.return_value = mock_url_obj
  mock_cache_repo.increase_click_count.return_value = 1

  result = url_service.redirect(mock_url_obj.short_code)

  assert result == mock_url_obj.long_url
  assert mock_cache_repo.get_by_short_code.assert_called_once
  assert mock_cache_repo.set_url_obj.assert_not_called
  assert mock_cache_repo.increase_click_count.assert_called_once

def test_redirect_in_db(mock_cache_repo, mock_db_repo, mock_url_obj, url_service):
  mock_cache_repo.get_by_short_code.return_value = None
  mock_db_repo.get_by_short_code.return_value = mock_url_obj
  mock_cache_repo.set_url_obj.return_value = True
  mock_cache_repo.increase_click_count.return_value = 1

  result = url_service.redirect(mock_url_obj.short_code)

  assert result == mock_url_obj.long_url
  assert mock_cache_repo.get_by_short_code.assert_called_once
  assert mock_db_repo.get_by_short_code.assert_called_once
  assert mock_cache_repo.set_url_obj.assert_called_once
  assert mock_cache_repo.increase_click_count.assert_called_once

def test_redirect_not_found(mock_cache_repo, mock_db_repo, url_service, mock_url_obj):
  mock_cache_repo.get_by_short_code.return_value = None
  mock_db_repo.get_by_short_code.return_value = None

  with pytest.raises(HTTPException) as exc:
    url_service.redirect(mock_url_obj.short_code)

  assert exc.value.status_code == 404
  assert exc.value.detail == "Short code not found"
  assert mock_cache_repo.get_by_short_code.assert_called_once
  assert mock_db_repo.get_by_short_code.assert_called_once
  assert mock_cache_repo.set_url_obj.assert_not_called
  assert mock_cache_repo.increase_click_count.assert_not_called