from fastapi.exceptions import HTTPException
import pytest
from sqlalchemy.exc import IntegrityError

from app.core.exceptions import ShortCodeGenerationError, UrlNotFoundError
from tests.fixtures.url_service_fixture import mock_url_obj, create_url_obj, mock_db_repo, mock_cache_repo, mock_config, url_service, mock_short_url, mock_input_short_url

@pytest.mark.unit
def test_get_or_create_get_success(mock_db_repo, mock_url_obj, create_url_obj, url_service):
  mock_db_repo.get_by_long_url.return_value = mock_url_obj

  result = url_service.get_or_create(create_url_obj)

  assert result.id == mock_url_obj.id
  assert result.long_url == mock_url_obj.long_url
  assert result.short_code == mock_url_obj.short_code
  assert mock_db_repo.get_by_long_url.call_count == 1
  assert mock_db_repo.save.call_count == 0

@pytest.mark.unit
def test_get_or_create_create_success(mock_db_repo, mock_url_obj, create_url_obj, url_service):
  mock_db_repo.get_by_long_url.return_value = None
  mock_db_repo.save.return_value = mock_url_obj

  result = url_service.get_or_create(create_url_obj)

  assert result.id == mock_url_obj.id
  assert result.long_url == mock_url_obj.long_url
  assert result.short_code == mock_url_obj.short_code
  assert mock_db_repo.get_by_long_url.call_count == 1
  assert mock_db_repo.save.call_count == 1

@pytest.mark.unit
def test_get_or_create_short_url_as_input(mock_db_repo, mock_config, mock_url_obj, mock_input_short_url, url_service):
  mock_config.NETLOC = "127.0.0.1:8000"
  mock_db_repo.get_by_short_code.return_value = mock_url_obj

  result = url_service.get_or_create(mock_input_short_url)

  assert result.long_url == mock_url_obj.long_url
  assert mock_db_repo.get_by_short_code.call_count == 1  

@pytest.mark.unit
def test_get_or_create_race_condition(mock_db_repo, mock_url_obj, create_url_obj, url_service):
  mock_db_repo.get_by_long_url.return_value = None
  mock_db_repo.save.side_effect = [IntegrityError("stmt", "params", "orig"), mock_url_obj]

  result = url_service.get_or_create(create_url_obj)

  assert result.id == mock_url_obj.id
  assert result.long_url == mock_url_obj.long_url
  assert result.short_code == mock_url_obj.short_code
  assert mock_db_repo.save.call_count == 2
  assert mock_db_repo.get_by_long_url.call_count == 2

@pytest.mark.unit
def test_get_or_create_race_condition_fail(mock_db_repo, create_url_obj, url_service):
  mock_db_repo.get_by_long_url.return_value = None
  mock_db_repo.save.side_effect = IntegrityError("stmt", "params", "orig")

  with pytest.raises(ShortCodeGenerationError) as exc:
    url_service.get_or_create(create_url_obj)

  assert f"Failed to generate a unique code for '{create_url_obj.long_url}' URL" in str(exc.value)
  assert mock_db_repo.save.call_count == 5
  assert mock_db_repo.get_by_long_url.call_count == 6

@pytest.mark.unit
def test_fetch_long_url_in_cache(mock_cache_repo, mock_url_obj, url_service):
  mock_cache_repo.get_by_short_code.return_value = mock_url_obj

  result = url_service.fetch_long_url(mock_url_obj.short_code)

  assert result.long_url == mock_url_obj.long_url
  assert mock_cache_repo.get_by_short_code.call_count == 1

@pytest.mark.unit
def test_fetch_long_url_in_db(mock_cache_repo, mock_db_repo, mock_url_obj, url_service):
  mock_cache_repo.get_by_short_code.return_value = None
  mock_db_repo.get_by_short_code.return_value = mock_url_obj
  mock_cache_repo.set_url_obj.return_value = True

  result = url_service.fetch_long_url(mock_url_obj.short_code)

  assert result.long_url == mock_url_obj.long_url
  assert mock_cache_repo.get_by_short_code.call_count == 1
  assert mock_db_repo.get_by_short_code.call_count == 1
  assert mock_cache_repo.set_url_obj.call_count == 1

@pytest.mark.unit
def test_fetch_long_url_not_found(mock_cache_repo, mock_db_repo, url_service, mock_url_obj):
  mock_cache_repo.get_by_short_code.return_value = None
  mock_db_repo.get_by_short_code.return_value = None

  with pytest.raises(UrlNotFoundError) as exc:
    url_service.fetch_long_url(mock_url_obj.short_code)

  assert f"Short code '{mock_url_obj.short_code}' not found" in str(exc.value)
  assert mock_cache_repo.get_by_short_code.call_count == 1
  assert mock_db_repo.get_by_short_code.call_count == 1
  assert mock_cache_repo.set_url_obj.call_count == 0

@pytest.mark.unit
def test_fetch_stats_success(mock_db_repo, mock_url_obj, url_service, mock_short_url):
  mock_db_repo.get_by_short_code.return_value = mock_url_obj

  result = url_service.fetch_stats(mock_short_url)

  assert result.short_code == mock_url_obj.short_code
  assert mock_db_repo.get_by_short_code.call_count == 1

@pytest.mark.unit
def test_fetch_stats_short_url_not_found(mock_db_repo, url_service, mock_short_url):
  mock_db_repo.get_by_short_code.return_value = None

  with pytest.raises(UrlNotFoundError) as exc:
    url_service.fetch_stats(mock_short_url)

  assert f"Short URL '{mock_short_url}' not found" in str(exc.value)
  assert mock_db_repo.get_by_short_code.call_count == 1