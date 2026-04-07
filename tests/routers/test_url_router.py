from app.core.exceptions import ShortCodeGenerationError, UrlNotFoundError
from tests.fixtures.url_router_fixture import client, mock_url_service, mock_url_obj, mock_short_url

def test_create_short_url_success(client, mock_url_service, mock_url_obj):
  mock_url_service.get_or_create.return_value = mock_url_obj

  result = client.post("/shorten", json={"long_url": "https://example.com"})
  data = result.json()

  assert result.status_code == 200
  assert data["short_url"].endswith(f"/{mock_url_obj.short_code}")
  assert mock_url_service.get_or_create.call_count == 1

def test_create_short_url_failure(client, mock_url_service, mock_url_obj):
  mock_url_service.get_or_create.side_effect = ShortCodeGenerationError

  result = client.post("/shorten", json={"long_url": "https://example.com"})
  data = result.json()

  assert result.status_code == 500
  assert data["detail"] == "Failed to generate unique code"
  assert mock_url_service.get_or_create.call_count == 1

def test_fetch_long_url_success(client, mock_url_service, mock_url_obj):
  mock_url_service.fetch_long_url.return_value = mock_url_obj

  result = client.get(f"/{mock_url_obj.short_code}", follow_redirects=False)

  assert result.status_code == 307
  assert result.headers["location"] == mock_url_obj.long_url
  assert mock_url_service.fetch_long_url.call_count == 1

def test_fetch_long_url_not_found(client, mock_url_obj, mock_url_service):
  mock_url_service.fetch_long_url.side_effect = UrlNotFoundError

  result = client.get(f"/{mock_url_obj.short_code}", follow_redirects=False)
  data = result.json()

  assert result.status_code == 404
  assert data["detail"] == "Short URL not found"
  assert mock_url_service.fetch_long_url.call_count == 1

def test_fetch_stats_success(client, mock_url_service, mock_url_obj, mock_short_url):
  mock_url_service.fetch_stats.return_value = mock_url_obj

  result = client.get(f"/stats/{mock_short_url}")
  data = result.json()

  assert result.status_code == 200
  assert data["click_count"] == mock_url_obj.click_count
  assert mock_url_service.fetch_stats.call_count == 1

def test_fetch_stats_short_url_not_found(client, mock_url_service, mock_short_url):
  mock_url_service.fetch_stats.side_effect = UrlNotFoundError(f"Short URL '{mock_short_url}' not found")

  result = client.get(f"/stats/{mock_short_url}")
  data = result.json()

  assert result.status_code == 404
  assert data["detail"] == "Short URL not found"
  assert mock_url_service.fetch_stats.call_count == 1