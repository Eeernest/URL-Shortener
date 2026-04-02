from tests.fixtures.url_router_fixture import client, mock_url_service, mock_url_obj

from app.core.exceptions import ShortCodeGenerationError, UrlNotFoundError

def test_create_short_url_success(client, mock_url_service, mock_url_obj):
  mock_url_service.get_or_create.return_value = mock_url_obj

  result = client.post("/shorten", json={"long_url": "https://example.com"})
  data = result.json()

  assert result.status_code == 200
  assert data["short_url"].endswith(f"/{mock_url_obj.short_code}")
  assert mock_url_service.get_or_create.call_count == 1

def test_create_short_url_failure(client, mock_url_service, mock_url_obj):
  mock_url_service.get_or_create.side_effect = ShortCodeGenerationError(f"Failed to generate a unique code for '{mock_url_obj.short_code}' URL")

  result = client.post("/shorten", json={"long_url": "https://example.com"})
  data = result.json()

  assert result.status_code == 500
  assert data["detail"] == f"Failed to generate a unique code for '{mock_url_obj.short_code}' URL"
  assert mock_url_service.get_or_create.call_count == 1

def test_fetch_long_url_success(client, mock_url_service, mock_url_obj):
  mock_url_service.fetch_long_url.return_value = mock_url_obj

  result = client.get(f"/{mock_url_obj.short_code}", follow_redirects=False)

  assert result.status_code == 307
  assert result.headers["location"] == mock_url_obj.long_url
  assert mock_url_service.fetch_long_url.call_count == 1

def test_fetch_long_url_not_found(client, mock_url_obj, mock_url_service):
  mock_url_service.fetch_long_url.side_effect = UrlNotFoundError(f"Short code '{mock_url_obj.short_code}' not found")

  result = client.get(f"/{mock_url_obj.short_code}", follow_redirects=False)
  data = result.json()

  assert result.status_code == 404
  assert data["detail"] == "Short code not found"
  assert mock_url_service.fetch_long_url.call_count == 1