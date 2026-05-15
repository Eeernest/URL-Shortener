import pytest

from tests.fixtures.url_cache_fixture import url_cache_repo, create_url_obj, saved_url_obj

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_by_short_code(url_cache_repo, saved_url_obj):
  result = await url_cache_repo.get_by_short_code(saved_url_obj.short_code)

  assert result is not None
  assert result.long_url == saved_url_obj.long_url
  assert result.short_code == saved_url_obj.short_code

@pytest.mark.anyio
@pytest.mark.integration
async def test_set_url_obj(url_cache_repo, create_url_obj):
  result = await url_cache_repo.set_url_obj(create_url_obj)

  assert result is True