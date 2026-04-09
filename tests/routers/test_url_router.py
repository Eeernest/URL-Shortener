from app.core.exceptions import ShortCodeGenerationError, UrlNotFoundError
from tests.fixtures.url_router_fixture import mock_client, mock_url_service, mock_url_obj, mock_short_url, integration_client, integration_service, payload_long_url

def test_create_short_url_success(mock_client, mock_url_service, mock_url_obj):
  mock_url_service.get_or_create.return_value = mock_url_obj

  result = mock_client.post("/shorten", json={"long_url": mock_url_obj.long_url})
  data = result.json()

  assert result.status_code == 200
  assert data["short_url"].endswith(f"/{mock_url_obj.short_code}")
  assert mock_url_service.get_or_create.call_count == 1

def test_create_short_url_failure(mock_client, mock_url_service, mock_url_obj):
  mock_url_service.get_or_create.side_effect = ShortCodeGenerationError

  result = mock_client.post("/shorten", json={"long_url": mock_url_obj.long_url})
  data = result.json()

  assert result.status_code == 500
  assert data["detail"] == "Failed to generate unique code"
  assert mock_url_service.get_or_create.call_count == 1

def test_create_short_url_wrong_input_failure(mock_client):
  result = mock_client.post("/shorten", json={"long_url": "not valid url"})
  data = result.json()

  assert result.status_code == 422
  assert data["detail"] == "Wrong input data"

def test_fetch_long_url_success(mock_client, mock_url_service, mock_url_obj):
  mock_url_service.fetch_long_url.return_value = mock_url_obj

  result = mock_client.get(f"/{mock_url_obj.short_code}", follow_redirects=False)

  assert result.status_code == 307
  assert result.headers["location"] == mock_url_obj.long_url
  assert mock_url_service.fetch_long_url.call_count == 1

def test_fetch_long_url_not_found(mock_client, mock_url_obj, mock_url_service):
  mock_url_service.fetch_long_url.side_effect = UrlNotFoundError

  result = mock_client.get(f"/{mock_url_obj.short_code}", follow_redirects=False)
  data = result.json()

  assert result.status_code == 404
  assert data["detail"] == "Short URL not found"
  assert mock_url_service.fetch_long_url.call_count == 1

def test_fetch_stats_success(mock_client, mock_url_service, mock_url_obj, mock_short_url):
  mock_url_service.fetch_stats.return_value = mock_url_obj

  result = mock_client.get(f"/stats/{mock_short_url}")
  data = result.json()

  assert result.status_code == 200
  assert data["click_count"] == mock_url_obj.click_count
  assert mock_url_service.fetch_stats.call_count == 1

def test_fetch_stats_short_url_not_found(mock_client, mock_url_service, mock_short_url):
  mock_url_service.fetch_stats.side_effect = UrlNotFoundError

  result = mock_client.get(f"/stats/{mock_short_url}")
  data = result.json()

  assert result.status_code == 404
  assert data["detail"] == "Short URL not found"
  assert mock_url_service.fetch_stats.call_count == 1

def test_url_lifecycle_happy_path(integration_client, payload_long_url):
  create_short_url_result = integration_client.post("/shorten", json=payload_long_url)
  create_short_url_data = create_short_url_result.json()

  assert create_short_url_result.status_code == 200
  assert "short_url" in create_short_url_data

  short_url = create_short_url_data["short_url"]
  short_code = short_url.split("/")[-1]

  fetch_long_url_result = integration_client.get(f"/{short_code}", follow_redirects=False)

  assert fetch_long_url_result.status_code == 307
  assert fetch_long_url_result.headers["location"] == payload_long_url["long_url"]