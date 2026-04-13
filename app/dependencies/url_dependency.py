from app.core.config import Config
from app.db.url_db import SessionDep
from app.caches.url_cache import RedisDep
from app.repositories.url_db_repository import UrlDbRepository
from app.repositories.url_cache_repository import UrlCacheRepository
from app.services.url_service import UrlService

from typing import Annotated
from fastapi import Depends

def get_url_service(session: SessionDep, cache: RedisDep):
  config = Config()
  db_repo = UrlDbRepository(session)
  cache_repo = UrlCacheRepository(cache, config)

  return UrlService(db_repo, cache_repo, config)

UrlDep = Annotated[UrlService, Depends(get_url_service)]