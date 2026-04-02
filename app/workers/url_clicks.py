from app.core.config import Config
from app.db.url_db import SessionDep
from app.caches.url_cache import RedisDep
from app.repositories.url_db_repository import UrlDbRepository
from app.repositories.url_cache_repository import UrlCacheRepository

import time

def sync_clicks(cache_repo: UrlCacheRepository, db_repo: UrlDbRepository):
  clicks = cache_repo.get_click_count()

  for short_code, count in clicks.items():
    db_repo.increase_click_count(short_code, int(count))

  cache_repo.clear_click_count()

def run():
  session = next(SessionDep())
  redis = next(RedisDep())

  db_repo = UrlDbRepository(session)
  cache_repo = UrlCacheRepository(redis, Config)

  while True:
    sync_clicks(cache_repo, db_repo)
    time.sleep(5)

if __name__ == "__main__":
  run()